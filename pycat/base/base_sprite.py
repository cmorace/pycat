"""The base_sprite module defines the BaseSprite class."""

from enum import Enum, auto
from random import uniform
from typing import List, Optional, Set, Tuple, Union

from pycat.base.color import Color
from pycat.base.event.window_event_subscriber import WindowEventSubscriber
from pycat.base.image import Animation, Image, Texture
from pycat.geometry.point import Point
from pycat.math import (get_degrees_from_direction,
                        get_direction_from_degrees,
                        get_distance, get_rotated_point)

from pyglet.sprite import Sprite as PygletSprite
from pyglet.graphics import OrderedGroup


class RotationMode(Enum):
    """Sets the behavior of a sprite's image rotation.

    - NO_ROTATION: Image rotation remains fixed.
    - RIGHT_LEFT: Image is reflected across the y-axis
    - MIRROR: Image is reflected across the x-axis
    - ALL_AROUND: Image rotation matches sprite rotation
    """
    NO_ROTATION = auto()
    RIGHT_LEFT = auto()
    MIRROR = auto()
    ALL_AROUND = auto()


class BaseSprite(WindowEventSubscriber):
    """A Sprite is an image displayed on screen.

    It can also listen for window events by overriding the methods
    defined in `WindowEventListener` and adding it to a window via
    a window's `add_window_event_subscriber()`
    """

    _default_image = Image.get_solid_color_texture(1, 1)

    def __init__(self,
                 image: Union[Animation, Texture] = _default_image,
                 x: float = 0,
                 y: float = 0,
                 layer: int = 0):
        """Instantiate a new Sprite."""
        self.__layer = layer
        self.rotation_mode = RotationMode.ALL_AROUND
        self._sprite = PygletSprite(image,
                                    x, y,
                                    subpixel=True,
                                    group=OrderedGroup(layer))
        self.__tags: Set[str] = set()
        self.__image_file = ""
        self.__rotation = 0.0
        self.__is_right_facing = True
        self.__forward_direction = get_direction_from_degrees(self.__rotation)

    @classmethod
    def create_from_file(cls,
                         file: str,
                         x: float = 0,
                         y: float = 0,
                         layer: int = 0):
        """Class method to create a sprite from file"""
        sprite = cls(Image.get_image_from_file(file), x, y, layer)
        sprite.__image_file = file
        return sprite

    @classmethod
    def create_from_color(cls,
                          color: Tuple[int, int, int, int]
                          = (255, 255, 255, 255),
                          x: float = 0,
                          y: float = 0,
                          width: int = 1,
                          height: int = 1,
                          layer: int = 0):
        return cls(Image.get_solid_color_texture(width, height, color), x, y,
                   layer)

    ##################################################################
    # Built-in
    ##################################################################

    def __str__(self):
        return ('Sprite with image '+self.image
                + ' at position ('+str(self.x)+','+str(self.y)
                + ') with tags: '+', '.join(self.tags))

    def __lt__(self, other: 'BaseSprite') -> bool:
        return self.__layer < other.__layer

    ##################################################################
    # Sprite Position
    ##################################################################

    @property
    def x(self) -> float:
        """The sprite's x coordinate."""
        return self._sprite.x

    @x.setter
    def x(self, x: float):
        self._sprite.x = x

    @property
    def y(self) -> float:
        """The sprite's y coordinate."""
        return self._sprite.y

    @y.setter
    def y(self, y: float):
        self._sprite.y = y

    @property
    def position(self) -> Point:
        """The sprite's center (x,y) position."""
        return Point(self._sprite.x, self._sprite.y)

    @position.setter
    def position(self, p: Union[Point, Tuple[float, float]]):
        if isinstance(p, Point):
            self._sprite.x = p.x
            self._sprite.y = p.y
        else:
            self._sprite.x, self._sprite.y = p

    def limit_position_to_area(
            self,
            min_x: float,
            max_x: float,
            min_y: float,
            max_y: float
            ):
        """Restrict the sprite's position to a rectangular region."""
        if self.x < min_x:
            self.x = min_x
        elif self.x > max_x:
            self.x = max_x
        if self.y < min_y:
            self.y = min_y
        elif self.y > max_y:
            self.y = max_y

    ##################################################################
    # Sprite Rotation
    ##################################################################

    @property
    def rotation(self) -> float:
        """Current orientation of the sprite in degrees.

        Rotation is counter-clockwise positive
        Note that the rotation of the sprite's image may not
        correspond to the actual rotation value if the RotationMode
        is set to RIGHT_LEFT or NO_ROTATION
        """
        return self.__rotation

    @rotation.setter
    def rotation(self, degrees: float):
        self.__rotation = degrees
        self.__forward_direction = get_direction_from_degrees(self.__rotation)
        if self.rotation_mode is RotationMode.ALL_AROUND:
            self.image_rotation = degrees
        elif self.rotation_mode is RotationMode.RIGHT_LEFT:
            rotation = degrees % 360
            # 90 or 270 degree rotations maintain previous orientation
            if (90 < rotation < 270) and self.__is_right_facing:
                self.scale_x *= -1
                self.__is_right_facing = False
            elif ((rotation < 90 or rotation > 270)
                  and not self.__is_right_facing):
                self.scale_x *= -1
                self.__is_right_facing = True
        elif self.rotation_mode is RotationMode.MIRROR:
            self.image_rotation = degrees % 360
            # 90 or 270 degree rotations maintain previous orientation
            if (90 < self.image_rotation < 270) and self.__is_right_facing:
                self.scale_y *= -1
                self.__is_right_facing = False
            elif ((self.image_rotation < 90 or self.image_rotation > 270)
                  and not self.__is_right_facing):
                self.scale_y *= -1
                self.__is_right_facing = True

    @property
    def image_rotation(self) -> float:
        # rotation is clock-wise positive in pyglet
        return -self._sprite.rotation

    @image_rotation.setter
    def image_rotation(self, degrees: float):
        # rotation is clock-wise positive in pyglet
        self._sprite.rotation = -degrees

    @property
    def layer(self) -> int:
        return self.__layer

    @layer.setter
    def layer(self, layer: int):
        self.__layer = layer
        self._sprite.group = OrderedGroup(layer)
        if self._sprite.batch:
            self._sprite.batch.invalidate()

    ##################################################################
    # Tags
    ##################################################################

    def add_tag(self, tag: str):
        if tag in self.__tags:
            print('Sprite tag warning: tried to add tag "' + tag +
                  '" but it already exists')
        else:
            self.__tags.add(tag)

    def remove_tag(self, tag: str):
        if tag not in self.__tags:
            print('Sprite tag warning: tried to remove tag "' + tag +
                  '" but it does not exist')
        else:
            self.__tags.remove(tag)

    def clear_tags(self):
        self.__tags.clear()

    @property
    def tags(self) -> Set[str]:
        """User defined tags, read-only."""
        return self.__tags

    ##################################################################
    # Sprite Appearance
    ##################################################################

    @property
    def scale(self) -> float:
        """The scale of the sprite.

        If the sprite's current scale is 1 then its size on screen
        will match the pixel dimensions of its image.
        """
        return self._sprite.scale

    @scale.setter
    def scale(self, scale: float):
        self._sprite.scale = scale

    def scale_to_width(self, new_width: float):
        self.scale *= new_width/self.width

    def scale_to_height(self, new_height: float):
        self.scale *= new_height/self.height

    @property
    def scale_x(self) -> float:
        """The sprite's scale in its local x-direction.

        Setting the `scale_x` property will shrink/stretch the image
        along the sprite's horizontal axis. Negative values will flip
        the image across it's vertical axis
        """
        return self._sprite.scale_x

    @scale_x.setter
    def scale_x(self, scale_x: float):
        self._sprite.scale_x = scale_x

    @property
    def scale_y(self) -> float:
        """The sprite's scale in its local y-direction.

        Setting the `scale_y` property will shrink/stretch the image
        along the sprite's vertical axis. Negative values will flip
        the image across it's horizontal axis
        """
        return self._sprite.scale_y

    @scale_y.setter
    def scale_y(self, scale_y: float):
        self._sprite.scale_y = scale_y

    @property
    def is_visible(self) -> bool:
        """If `is_visible` is False, the sprite will not be drawn."""
        return self._sprite.visible

    @is_visible.setter
    def is_visible(self, is_visible: bool):
        self._sprite.visible = is_visible

    @property
    def color(self) -> Color.RGB:
        """The sprite's (Red, Green, Blue) values.

        Changes the tint of the sprite image. RGB values in [0,255] range
        """
        return Color.RGB(*self._sprite.color)

    @color.setter
    def color(self, color: Color.RGB):
        self._sprite.color = color

    def set_random_color(self):
        self.color = Color.random_rgb()

    @property
    def opacity(self) -> int:
        """Opacity (transparency) value.

        Opacity values are in [0, 255] range where, 0 is
        fully transparent and 255 is non-transparent.
        """
        return self._sprite.opacity

    @opacity.setter
    def opacity(self, opacity: int):
        self._sprite.opacity = opacity

    @property
    def width(self) -> float:
        """The width of the displayed sprite image.

        The `width` property is updated if the sprite's
        `scale` is modified
        """
        return self._sprite.width

    @width.setter
    def width(self, new_width: float):
        self.scale_x *= new_width/self.width

    @property
    def height(self) -> float:
        """The height of the displayed sprite image.

        The `height` property is updated if the sprite's
        `scale` is modified
        """
        return self._sprite.height

    @height.setter
    def height(self, new_height: float):
        self.scale_y *= new_height/self.height

    @property
    def image(self) -> Optional[str]:
        """The name of the image file"""
        return self.__image_file

    @image.setter
    def image(self, file: Optional[str]):
        if file is not None:
            self.__image_file = file
            self.set_image_from_file(file)

    @property
    def texture(self) -> Optional[Texture]:
        if isinstance(self._sprite.image, Animation):
            return None
        else:
            return self._sprite.image

    @texture.setter
    def texture(self, texture: Texture):
        self._sprite.image = texture

    def set_image(self, image: Union[Animation, Texture]):
        """Set the Sprite's Texture or Animation"""
        self._sprite.image = image

    def set_image_from_file(self, file: str):
        """Set the Sprite's Texture or Animation from file"""
        self._sprite.image = Image.get_image_from_file(file)

    def change_animation_frame_duration(self, dt: float):
        """Change the animation speed if animated"""
        if isinstance(self._sprite.image, Animation):
            for frame in self._sprite.image.frames:
                frame.duration = max(frame.duration + dt, 0.01)

    def get_animation_frame_duration(self) -> List[float]:
        """Get a list of frame duration durations if animated"""
        if isinstance(self._sprite.image, Animation):
            return [frame.duration for frame in self._sprite.image.frames]
        else:
            return []

    def contains_point(self, p: Point) -> bool:
        """Returns True if point is on the Sprite's image, otherwise False."""
        d = Point(self.width, self.height) / 2
        c = self.position
        q = get_rotated_point(p - c, self._sprite.rotation)
        return (-d.x < q.x < d.x) and (-d.y < q.y < d.y)

    ##################################################################
    # Scratch language
    ##################################################################

    def move_forward(self, step_size: float):
        """Move the sprite forward by step_size pixels.

        The forward direction is based on a sprite's `self.rotation`.
        If `self.rotation = 0` then forward is facing right.
        """
        self.position += step_size * self.__forward_direction

    def goto(self, other_sprite: 'BaseSprite'):
        """Go to another Sprite's position."""
        self.position = other_sprite.position

    def goto_random_position_in_region(
            self,
            min_x: float = 0,
            min_y: float = 0,
            max_x: float = 0,
            max_y: float = 0
            ):
        """Go to a random point inside a rectangular region."""
        offset: Point = Point(self.width, self.height) / 2
        low_bound = Point(min_x, min_y) + offset
        up_bound = Point(max_x, max_y) - offset
        self.x = uniform(low_bound.x, up_bound.x)
        self.y = uniform(low_bound.y, up_bound.y)

    def point_toward(self, p: Point):
        """Change rotation to point towards point p."""
        self.rotation = get_degrees_from_direction(p - self.position)

    def point_toward_sprite(self, sprite: 'BaseSprite'):
        """Change rotation to point towards another sprite."""
        self.point_toward(sprite.position)

    def distance_to(self, point: Point) -> float:
        return get_distance(self.position, point)

    ##################################################################
    # Framework
    ##################################################################

    def draw(self):
        """Draws the sprite in a window's draw function"""
        self._sprite.draw()
