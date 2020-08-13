from typing import Tuple, Optional
from pyglet.sprite import Sprite as PygletSprite

from pycat.geometry.point import Point
from pycat.image import get_animation_from_file, get_texture_from_file, get_checker_texture
from pycat.math import get_direction_from_degrees
from pycat.debug import print_warning

from random import randint

class Sprite:

    def __init__(
        self, 
        img_file_path: Optional[str] = None, 
        x: float = 0, 
        y: float = 0,
        layer: int = 0,
    ):
        """The constructor loads an image or GIF animation and sets the
        initial (x,y) position of the sprite. Subclasses of the Sprite
        class can override the on_create method to initialize properties
        without needing to write a new __init__() method. Note that on_create
        is only called when the sprite is added to the Window or a SpriteList.

        Args:
            img_file_path (str): path to a bitmap image or GIF animation
            x (float, optional): initial x co-ordinate. Defaults to 0.
            y (float, optional): initial y co-ordinate. Defaults to 0.
        """
        if not img_file_path:
            img = get_checker_texture()
        elif img_file_path.endswith(".gif"):
            img = get_animation_from_file(img_file_path)
        else:
            img = get_texture_from_file(img_file_path)

        self._sprite: PygletSprite = PygletSprite(img, x=x, y=y)

        self._layer = layer

    ################################################################################
    # Override these to set the sprite's behavior
    ################################################################################

    def on_create(self):
        """Called (once) when added to a window.
        """
        pass

    def on_update(self, dt):
        """Called 60 times a second when added to a window. Stops being called when removed from window.
        """
        pass

    ################################################################################
    # Sprite Position
    ################################################################################

    @property
    def x(self) -> float:
        return self._sprite.x

    @x.setter
    def x(self, x: float):
        self._sprite.x = x

    @property
    def y(self) -> float:
        return self._sprite.y

    @y.setter
    def y(self, y: float):
        self._sprite.y = y

    @property
    def position(self) -> Point:
        return Point(self._sprite.x, self._sprite.y)        

    @position.setter
    def position(self, p: Point):
        self._sprite.x = p.x
        self._sprite.y = p.y

    def limit_position_to_area(self, min_x, max_x, min_y, max_y):
        if self.x < min_x:
            self.x = min_x
        elif self.x > max_x:
            self.x = max_x
        if self.y < min_y:
            self.y = min_y
        elif self.y > max_y:
            self.y = max_y

    def goto(self, other_sprite: 'Sprite'):
        self.position = other_sprite.position

    def goto_random_position(self, window: 'Window'):
        self.x = randint(0, window.width-self.width)
        self.y = randint(0, window.height-self.height)

    ################################################################################
    # Sprite Rotation
    ################################################################################

    @property
    def rotation(self) -> float:
        # rotation is clock-wise positive in pyglet
        return -self._sprite.rotation

    @rotation.setter
    def rotation(self, degrees: float):
        # rotation is clock-wise positive in pyglet
        self._sprite.rotation = -degrees

    def rotate(self, degrees: float):
        """rotates the sprite by degrees

        Args:
            degrees (float): positive direction is counter-clockwise
        """
        self._sprite.rotation -= degrees

    ################################################################################
    # Sprite Motion
    ################################################################################

    def translate(self, x: float, y: float):
        """Translates the sprite by (x,y)

        Args:
            x (float): the amount to translate along the x-direction
            y (float): the amount to translate along the y-direction
        """
        self._sprite.x += x
        self._sprite.y += y

    def move_forward(self, step_size: float):
        """move the sprite forward by step_size

        Args:
            step_size (float): measured in pixels
        """
        v = get_direction_from_degrees(self.rotation)
        self.translate(v.x * step_size, v.y * step_size)

    ################################################################################
    # Sprite Appearance
    ################################################################################

    @property
    def scale(self) -> float:
        return self._sprite.scale

    @scale.setter
    def scale(self, scale: float):
        self._sprite.scale = scale

    @property
    def scale_x(self) -> float:
        return self._sprite.scale_x

    @scale_x.setter
    def scale_x(self, scale_x: float):
        self._sprite.scale_x = scale_x

    @property
    def scale_y(self) -> float:
        return self._sprite.scale_y

    @scale_y.setter
    def scale_y(self, scale_y: float):
        self._sprite.scale_y = scale_y

    @property
    def is_visible(self) -> bool:
        return self._sprite.visible

    @is_visible.setter
    def is_visible(self, is_visible: bool):
        self._sprite.visible = is_visible

    @property
    def layer(self) -> int:
        return self._layer

    @layer.setter
    def layer(self, layer: int):
        self._layer = layer

    @property
    def color(self) -> Tuple:
        return self._sprite.color

    @color.setter
    def color(self, color: Tuple):
        self._sprite.color = color

    @property
    def opacity(self) -> int:
        """opacity measures transparency

        Returns:
            int: the transparency value in range [0,255]
            0 being fully transparent and 255 non-transparent
        """
        return self._sprite.opacity

    @opacity.setter
    def opacity(self, opacity: int):
        """sets the transparency

        Args:
            opacity (int): the transparency value in range [0,255]
            0 being fully transparent and 255 non-transparent
        """
        self._sprite.opacity = opacity

    @property
    def width(self) -> float:
        return self._sprite.width

    @property
    def height(self) -> float:
        return self._sprite.height

    def change_image(self, img_file_path: str):
        if img_file_path.endswith(".gif"):
            self._sprite.image = get_animation_from_file(img_file_path)
        else:
            self._sprite.image = get_texture_from_file(img_file_path)

    def set_animation_dt(self, dt: float):
        if self._sprite._animation:
            self._sprite._animate(dt)
        else:
            print_warning("this sprite has no animation")

    ################################################################################
    # Framework methods
    ################################################################################

    def draw(self):
        # draws on current window set by pyglet backend
        self._sprite.draw()

    
