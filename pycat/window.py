from threading import Lock
from typing import Callable, List, Optional, Set, TypeVar

from pycat.base.base_sprite import BaseSprite
from pycat.base.base_window import BaseWindow
from pycat.base.event.key_event import KeyEvent
from pycat.base.event.mouse_event import MouseButton, MouseEvent
from pycat.debug.draw import draw_sprite_rects
from pycat.label import Label
from pycat.scheduler import Scheduler
from pycat.sprite import Sprite

T = TypeVar('T')


class SpriteCreationError(Exception):
    pass


class Window(BaseWindow):
    def __init__(self,
                 width: int = 1280,
                 height: int = 640,
                 background_image: Optional[str] = None,
                 enforce_window_limits: bool = True,
                 draw_sprite_rects: bool = False,
                 title: str = ""):
        super().__init__(width, height, title)

        self.draw_fps = False
        self.draw_sprite_rects = draw_sprite_rects

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

        self.__sprites: List[Sprite] = list()
        self.__labels: List[Label] = list()

        # add new sprites to a separate list after update
        self.__new_sprites: List[Sprite] = list()
        self.__new_labels: List[Label] = list()

        self.__pre_draw: Optional[Callable[[None], None]] = None
        self.on_draw(self.__auto_draw)
        self.__post_draw: Optional[Callable[[None], None]] = None

        self.__game_loop_running = False

    ##################################################################
    # Label management
    ##################################################################
    def add_label(self, label: Label):
        self.__labels.append(label)

    # todo: use protocol for label_cls type
    def create_label(self, label_cls: Callable[..., T] = Label) -> T:
        label = label_cls()
        label.on_create()
        self.__new_labels.append(label)
        return label

    ##################################################################
    # Sprite management
    ##################################################################
    # todo: use protocol for sprite_cls type
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
                                'rotation']:
                raise SpriteCreationError("You may not set '" + arg_name +
                                          "' when creating a sprite")

        if 'tag' in kwargs and 'tags' in kwargs:
            raise SpriteCreationError(
                "You may not specify both 'tag' and 'tags'"
                "when creating a sprite")

        tags = kwargs.pop('tags', [])
        if 'tag' in kwargs:
            tags.append(kwargs.pop('tag'))

        # Create a class
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

        return sprite

    def delete_sprites_with_tag(self, tag):
        for sprite in self.__sprites:
            if tag in sprite.tags:
                sprite.delete()

    def get_sprites_with_tag(self, tag):
        return [s for s in self.__sprites if tag in s.tags]

    def get_all_sprites(self):
        return self.__sprites

    def dump_all_sprites(self):
        print('Number of sprites in window: '+str(len(self.__sprites))+'\n\t'
              + '\n\t'.join([str(s) for s in self.__sprites]))

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

    def set_pre_draw(self, pre_draw_func: Callable[[None], None]):
        self.__pre_draw = pre_draw_func

    def set_post_draw(self, post_draw_func: Callable[[None], None]):
        self.__post_draw = post_draw_func

    def __auto_draw(self):
        self.clear()

        if self.__pre_draw:
            self.__pre_draw()

        if self.__background_sprite:
            self.__background_sprite.draw()

        for sprite in self.__sprites:
            sprite.draw()

        if self.draw_sprite_rects:
            draw_sprite_rects(self.__sprites)

        for label in self.__labels:
            label.draw()

        if self.__post_draw:
            self.__post_draw()

        if self.draw_fps:
            self._fps_label.draw()

    ##################################################################
    # Key input
    ##################################################################
    # rename to is_key_pressed?
    def get_key(self, keycode: int) -> bool:
        return keycode in self.__keys

    # rename to is_key_down?
    def get_key_down(self, keycode: int) -> bool:
        return keycode in self.__keys_down

    # rename to is_key_up?
    def get_key_up(self, keycode: int) -> bool:
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

        self.__sprites.sort()
        self.__new_sprites.clear()

    def __add_new_labels(self):
        for label in self.__new_labels:
            self.__labels.append(label)

        self.__new_labels.clear()

    def __remove_old_sprites(self):
        self.__sprites = [
            sprite for sprite in self.__sprites if not sprite.is_deleted
        ]

    def __remove_old_labels(self):
        self.__labels = [
            label for label in self.__labels if not label.is_deleted
        ]

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

        self.__remove_old_sprites()
        self.__remove_old_labels()

        self.__add_new_sprites()
        self.__add_new_labels()

        if self.__enforce_window_limits:
            for sprite in self.__sprites:
                sprite.limit_position_to_area(0, self.width, 0, self.height)

        if self.draw_fps:
            self._fps_label.update()

    # todo: list out event kwargs
    def run(self, **kwargs):
        Scheduler.update(self.__game_loop)
        self.__game_loop_running = True
        super().run(**kwargs)
