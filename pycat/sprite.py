from typing import Tuple, Optional
from pyglet.sprite import Sprite as PygletSprite

from pycat.geometry.point import Point
from pycat.image import get_animation_from_file, get_texture_from_file, get_checker_texture
from pycat.math import get_direction_from_degrees
from pycat.debug import print_warning

from random import randint

class UnmanagedSprite:
    '''A Sprite that is not "managed" by a Window.
    '''    

    def __init__(
        self, 
        tags: [str] = [],
        call_on_create = True
    ):
        self.__tags = tags

        img = get_checker_texture()
        self._sprite: PygletSprite = PygletSprite(img)

        self._layer = 0

        if call_on_create:
            self.on_create()



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

    def set_image(self, img_file_path: str):
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
    # Scratch languge
    ################################################################################

    def change_x(self, step_size: int):
        self.x += step_size

    ################################################################################
    # Framework methods
    ################################################################################

    def draw(self):
        # draws on current window set by pyglet backend
        self._sprite.draw()

    def get_tags(self):
        return self.__tags



    

class Sprite(UnmanagedSprite):
    '''
        A Sprite that is "managed" by a Window. 
        Never instantiate this class directly, it may only be created by a Window. 
        The connection to a Window provides additional functionality.
    '''

    def __init__(
        self, 
        window,
        tags: [str] = []        
    ):        
        self.__window = window
        # Prevent UnmanagedSprite's __init__ from calling on_create, instead the Window will do it after everything (eg, tags) are setup.
        super().__init__(tags,call_on_create=False) 
        
    @property
    def window(self) -> float:
        return self.__window        

    def delete(self):
        self.__window.delete_sprite(self)

    def goto_random_position(self):
        self.x = randint(0, self.__window.width-self.width)
        self.y = randint(0, self.__window.height-self.height)

    def touching_window_edge(self) -> bool:
        return (
               self.x <= 0
            or self.x >= self.__window.width
            or self.y <= 0
            or self.y >= self.__window.height)

    def touching_any_sprite_with_tag(self, tag):
        '''
            Checks if this sprite is touching any other sprite with appropiate tag. 
            Note: only sprites registered with the same Window are checked.
        '''
        from pycat.collision import is_aabb_collision
        for s in self.__window.get_sprites_with_tag(tag):
            if is_aabb_collision(self, s):
                return True
        return False        
