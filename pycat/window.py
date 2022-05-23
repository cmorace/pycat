from threading import Lock
from typing import Callable, List, Optional, Protocol, Set, TypeVar, Union

from pyglet import shapes
from pyglet.gl import (GL_NEAREST, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                       glTexParameteri)

from pycat.base.base_sprite import BaseSprite
from pycat.base.base_window import BaseWindow
from pycat.base.color import Color
from pycat.base.event.key_event import KeyEvent
from pycat.base.event.mouse_event import MouseButton, MouseEvent
from pycat.base.graphics_batch import GraphicsBatch
from pycat.debug.draw import draw_sprite_rects
from pycat.geometry.point import Point
from pycat.label import Label
from pycat.shape import Arc, Circle, Line, Rectangle, Triangle
from pycat.sprite import Sprite


class Drawable(Protocol):
    def draw() -> None:
        ...


# TypeVar for returning subclassed types from on_create() methods
T = TypeVar('T', bound=Drawable)


class SpriteCreationError(Exception):
    pass


class LabelCreationError(Exception):
    pass


class SpriteWithTagDoesNotExist(Exception):
    def __init__(self, tag: str):
        self.tag = tag

    def __str__(self):
        return 'Sprite with tag: "'+self.tag+'" does not exist'


class Window(BaseWindow):
    def __init__(self,
                 width: int = 1280,
                 height: int = 640,
                 background_image: Optional[str] = None,
                 enforce_window_limits: bool = True,
                 draw_sprite_rects: bool = False,
                 is_sharp_pixel_scaling: bool = False,
                 title: str = ""):
        super().__init__(width, height, title)

        self.draw_sprite_rects = draw_sprite_rects
        self.__is_sharp_pixel_scaling = is_sharp_pixel_scaling

        self.__background_sprite: Optional[BaseSprite] = None
        self.background_image = background_image

        self.__enforce_window_limits = enforce_window_limits

        self.__keys_lock = Lock()
        self.__keys_async: Set[int] = set()
        self.__keys_down_async: Set[int] = set()
        self.__keys_up_async: Set[int] = set()
        self.__keys: Set[int] = set()
        self.__keys_down: Set[int] = set()
        self.__keys_up: Set[int] = set()

        self.subscribe(on_key_press=self.__on_key_press,
                       on_key_release=self.__on_key_release,
                       on_mouse_press=self.__on_mouse_press)

        self.__sprites: List[Sprite] = []
        self.__labels: List[Label] = []
        self.__drawables: List[Drawable] = []

        self.__graphics_batch: GraphicsBatch = GraphicsBatch()
        self.__batched_shapes: List[shapes._ShapeBase] = []

        # add new sprites/labels to a separate list after update
        self.__new_sprites: List[Sprite] = []
        self.__new_labels: List[Label] = []

        self.__game_loop_running = False

    ##################################################################
    # Label management
    ##################################################################

    # todo: use protocol for label_cls type
    def create_label(
            self,
            label_cls: Callable[..., T] = Label,
            **kwargs
            ) -> T:

        # Sanity check kwargs
        for arg_name in kwargs:
            if arg_name not in ['x', 'y', 'text', 'font_size', 'font', 'color',
                                'opacity', 'position', 'layer']:
                raise LabelCreationError("You may not set '" + arg_name +
                                         "' when creating a label")

        # Create an object
        label = label_cls()
        label.y = self.height  # default y set to top of window
        label.on_create()

        # Add to window
        self.__new_labels.append(label)
        if not self.__game_loop_running:
            self.__add_new_labels()

        # Override properties
        for arg_name, arg_value in kwargs.items():
            setattr(label, arg_name, arg_value)
        if self.__is_sharp_pixel_scaling:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        return label

    def delete_all_labels(self):
        for label in self.get_all_labels():
            label.delete()

    def get_all_labels(self):
        return (
            [label for label in self.__labels if not label.is_deleted] +
            [label for label in self.__new_labels if not label.is_deleted]
        )

    ##################################################################
    # Sprite management
    ##################################################################

    def create_sprite(
            self,
            sprite_cls: Callable[..., T] = Sprite,
            **kwargs
            ) -> T:
        # Sanity check kwargs
        for arg_name in kwargs:
            if arg_name not in ['tag',
                                'tags',
                                'image',
                                'x',
                                'y',
                                'scale',
                                'scale_x',
                                'scale_y',
                                'color',
                                'layer',
                                'position',
                                'rotation',
                                'opacity',
                                'texture',
                                'is_visible']:
                raise SpriteCreationError("You may not set '" + arg_name +
                                          "' when creating a sprite")

        if 'tag' in kwargs and 'tags' in kwargs:
            raise SpriteCreationError(
                "You may not specify both 'tag' and 'tags'"
                "when creating a sprite")

        tags = kwargs.pop('tags', [])
        if 'tag' in kwargs:
            tags.append(kwargs.pop('tag'))

        # Create an object
        sprite = sprite_cls(window=self)
        sprite.on_create()

        # Add to window
        self.__new_sprites.append(sprite)
        if not self.__game_loop_running:
            self.__add_new_sprites()

        # Override properties
        for arg_name, arg_value in kwargs.items():
            setattr(sprite, arg_name, arg_value)
        if tags:
            sprite.clear_tags()
            for tag in tags:
                sprite.add_tag(tag)

        self.__graphics_batch.add_sprite(sprite)
        if self.__is_sharp_pixel_scaling:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return sprite

    def delete_all_sprites(self):
        for sprite in self.get_all_sprites():
            sprite.delete()

    def delete_sprites_with_tag(self, tag: str):
        for sprite in self.get_sprites_with_tag(tag):
            sprite.delete()

    def get_sprite_with_tag(self, tag: str) -> Sprite:
        sprites = self.get_sprites_with_tag(tag)
        if len(sprites) == 0:
            raise SpriteWithTagDoesNotExist(tag)
        return sprites[0]

    def get_sprites_with_tag(self, tag: str) -> List[Sprite]:
        return (
         [s for s in self.__sprites if tag in s.tags and not s.is_deleted] +
         [s for s in self.__new_sprites if tag in s.tags and not s.is_deleted]
        )

    def get_all_sprites(self) -> List[Sprite]:
        return (
            [s for s in self.__sprites if not s.is_deleted] +
            [s for s in self.__new_sprites if not s.is_deleted]
        )

    def dump_all_sprites(self):
        def as_str(sprite: Sprite):
            s = ''
            s += 'New ' if sprite in self.__new_sprites else ''
            s += 'Del' if sprite.is_deleted else ''
            s += '\t' + str(sprite)
            return s
        debug_sprite_list = self.__sprites + self.__new_sprites
        print('Number of sprites in window: '+str(len(debug_sprite_list)) +
              '\n\t\n\t'.join([as_str(s) for s in debug_sprite_list]))

    ##################################################################
    # Shape management
    ##################################################################

    def create_line(
        self,
        x1: float = 0, y1: float = 0,
        x2: float = 100, y2: float = 100,
        width=1,
        color: Color = Color.WHITE
    ) -> Line:

        a = Point(x1, y1)
        b = Point(x2, y2)
        line = Line(a, b, width, color=color, batch=self.__graphics_batch)
        self.__batched_shapes.append(line)  # no reference -> gc collects
        return line

    def create_triangle(
        self,
        x1: float = 0, y1: float = 0,
        x2: float = 100, y2: float = 0,
        x3: float = 50, y3: float = 86.6,
        color: Color = Color.WHITE
    ) -> Triangle:

        a = Point(x1, y1)
        b = Point(x2, y2)
        c = Point(x3, y3)
        tri = Triangle(a, b, c, color,
                       batch=self.__graphics_batch)
        self.__batched_shapes.append(tri)  # no reference -> gc collects
        return tri

    def create_circle(
        self,
        x: float = 0,
        y: float = 0,
        radius: float = 100,
        color: Color = Color.WHITE
    ) -> Circle:

        c = Circle(Point(x, y), radius, color=color,
                   batch=self.__graphics_batch)
        self.__batched_shapes.append(c)  # no reference -> gc collects
        return c

    def create_arc(
        self,
        x: float = 0,
        y: float = 0,
        radius: float = 360,
        segments: int = None,
        angle: float = shapes.math.tau,
        start_angle: float = 0,
        is_closed: bool = False,
        color: Color = Color.WHITE
    ) -> Arc:

        c = Arc(Point(x, y), radius, segments=segments, angle=angle,
                start_angle=start_angle, is_closed=is_closed, color=color,
                batch=self.__graphics_batch)
        self.__batched_shapes.append(c)  # no reference -> gc collects
        return c

    def create_rect(
        self,
        x: float,
        y: float,
        width: float = 100,
        height: float = 100,
        color: Color = Color.WHITE
    ) -> Rectangle:

        r = Rectangle(Point(x, y), width, height, color=color,
                      batch=self.__graphics_batch)
        self.__batched_shapes.append(r)  # no reference -> gc collects
        return r

    def add_drawable(
        self,
        drawable: T
    ) -> T:
        self.__drawables.append(drawable)
        return drawable

    def clear_drawables(self):
        self.__drawables.clear()
        for shape in self.__batched_shapes:
            shape.delete()
        self.__batched_shapes.clear()

    ##################################################################
    # Background sprite
    ##################################################################

    @property
    def background_sprite(self) -> Optional[BaseSprite]:
        return self.__background_sprite

    @property
    def background_image(self) -> Optional[str]:
        if self.__background_sprite:
            return self.__background_sprite.image
        return None

    @background_image.setter
    def background_image(self, file: Optional[str]):
        if file is not None:
            if self.__background_sprite is not None:
                self.__background_sprite.image = file
            else:
                self.__background_sprite = BaseSprite.create_from_file(file)
                self.__background_sprite.position = self.center

    ##################################################################
    # Drawing
    ##################################################################

    def __auto_draw(self):
        if self.__is_sharp_pixel_scaling:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.clear()

        if self.__background_sprite:
            self.__background_sprite.draw()

        self.__graphics_batch.draw()

        if self.draw_sprite_rects:
            draw_sprite_rects(self.__sprites)

        for drawable in self.__drawables:
            drawable.draw()

    ##################################################################
    # Key input
    ##################################################################

    def is_key_pressed(self, keycode: Union[int, str]) -> bool:
        if isinstance(keycode, str):
            keycode = ord(keycode)
        return keycode in self.__keys

    def is_key_down(self, keycode: Union[int, str]) -> bool:
        if isinstance(keycode, str):
            keycode = ord(keycode)
        return keycode in self.__keys_down

    def is_key_up(self, keycode: Union[int, str]) -> bool:
        if isinstance(keycode, str):
            keycode = ord(keycode)
        return keycode in self.__keys_up

    def __on_key_press(self, e: KeyEvent):
        with self.__keys_lock:
            self.__keys_down_async.add(e.symbol)
            self.__keys_async.add(e.symbol)

    def __on_key_release(self, e: KeyEvent):
        with self.__keys_lock:
            self.__keys_up_async.add(e.symbol)
            if e.symbol in self.__keys_async:
                self.__keys_async.remove(e.symbol)

    ##################################################################
    # Mouse input
    ##################################################################

    def __on_mouse_press(self, e: MouseEvent):
        p = e.position
        for sprite in self.__sprites:

            if sprite.contains_point(p):
                sprite.on_click(e)
                if e.button == MouseButton.LEFT:
                    sprite.on_left_click()

            sprite.on_click_anywhere(e)
            if e.button == MouseButton.LEFT:
                sprite.on_left_click_anywhere()

    ##################################################################
    # Runtime
    ##################################################################

    def __add_new_sprites(self):
        for sprite in self.__new_sprites:
            self.__sprites.append(sprite)
            self.__graphics_batch.add_sprite(sprite)

        self.__new_sprites.clear()

    def __add_new_labels(self):
        for label in self.__new_labels:
            self.__labels.append(label)
            self.__graphics_batch.add_label(label)

        self.__new_labels.clear()

    def __remove_old_sprites(self):
        new_sprite_list = []
        for s in self.__sprites:
            if s.is_deleted:
                self.__graphics_batch.remove_sprite(s)
            else:
                new_sprite_list.append(s)

        self.__sprites = new_sprite_list

    def __remove_old_labels(self):
        new_label_list = []
        for label in self.__labels:
            if label.is_deleted:
                self.__graphics_batch.remove_label(label)
            else:
                new_label_list.append(label)

        self.__labels = new_label_list

    def __game_loop(self, dt: float):
        # ensure all sprites will see the same set of keys this frame
        with self.__keys_lock:
            self.__keys = self.__keys_async.copy()

            # consume keys down
            self.__keys_down = self.__keys_down_async.copy()
            self.__keys_down_async.clear()

            # consume keys up
            self.__keys_up = self.__keys_up_async.copy()
            self.__keys_up_async.clear()

        for sprite in self.__sprites:
            sprite.on_update(dt)

        for label in self.__labels:
            label.on_update(dt)

        self.__add_new_sprites()
        self.__add_new_labels()

        self.__remove_old_sprites()
        self.__remove_old_labels()

        if self.__enforce_window_limits:
            for sprite in self.__sprites:
                sprite.limit_position_to_area(0, self.width, 0, self.height)
            for label in self.__labels:
                label.limit_position_to_area(0, self.width, 0, self.height)

    # todo: list out event kwargs
    def run(self,
            draw_function: Callable[[], None] = None,
            update_function: Callable[[float], None] = None,
            **kwargs):

        if draw_function is None:
            draw_function = self.__auto_draw

        if update_function is None:
            update_function = self.__game_loop
            self.__game_loop_running = True

        super().run(
            draw_function=draw_function,
            update_function=update_function,
            **kwargs)
