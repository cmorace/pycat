from typing import Tuple, Optional
from pyglet.sprite import Sprite as PygletSprite

from math import pi, sin, cos, sqrt, atan

from pycat.geometry.point import Point
from pycat.image import get_animation_from_file, get_texture_from_file, get_checker_texture
from pycat.math import get_direction_from_degrees, radian_to_degree, get_rotation_in_degrees_to_point_towards
from pycat.debug import print_warning

from random import randint

class UnmanagedSprite:
    '''A Sprite that is not "managed" by a Window.
    '''    

    def __init__(
        self, 
        tags: [str] = []
    ):
        self._tags = tags

        img = get_checker_texture()
        self._sprite: PygletSprite = PygletSprite(img)

        self._layer = 0

        self._image_file_path = ''


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

    def point_toward_sprite(self, sprite):
        self._sprite.rotation = get_rotation_in_degrees_to_point_towards(self.position, sprite.position)

    def point_toward_position(self, x, y):
        self._sprite.rotation = get_rotation_in_degrees_to_point_towards(self.position, Point(x,y))        

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

    @property
    def image(self) -> str:
        return self._image_file_path

    @image.setter
    def image(self, image_file_path: str):
        self._image_file_path = image_file_path
        if image_file_path.endswith(".gif"):
            self._sprite.image = get_animation_from_file(image_file_path)
        else:
            self._sprite.image = get_texture_from_file(image_file_path)

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
        return self._tags

    ################################################################################
    # Printing methods
    ################################################################################

    def __str__(self):
        return "Sprite '"+self._image_file_path+"' at ("+str(self.x)+', '+str(self.y)+')'

    

class Sprite(UnmanagedSprite):
    '''
        A Sprite that is "managed" by a Window. 
        Never instantiate this class directly, it may only be created by a Window. 
        The connection to a Window provides additional functionality.
        Primarially:
        - on_create is called when the sprite is added to the window
        - on_update is scheduled to be called 60 times a second
        - on_click is called when the sprite is clicked!
    '''

    def __init__(
        self, 
        window,
        tags: [str] = []     
    ):        
        self._window = window
        super().__init__(tags) 

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

    def on_click(self, x, y, button, modifiers):
        """Called when ANY mouse button is clicked while the cursor is over this sprite.
        """
        pass

    def on_left_click(self):
        """Simplified function signature for left clicks only.
        """
        pass


    ################################################################################
    # The rest
    ################################################################################


    @property
    def window(self) -> float:
        return self._window        

    def delete(self):
        self._window.delete_sprite(self)

    def goto_random_position(self):
        self.x = randint(0, self._window.width)
        self.y = randint(0, self._window.height)

    def touching_window_edge(self) -> bool:
        return (
               self.x <= 0
            or self.x >= self._window.width
            or self.y <= 0
            or self.y >= self._window.height)

    def touching_any_sprite(self):
        from pycat.collision import is_aabb_collision        
        for s in self._window.get_all_sprites():
            if self is not s and is_aabb_collision(self, s):
                return True
        return False             

    def touching_any_sprite_with_tag(self, tag):
        '''
            Checks if this sprite is touching any other sprite with appropiate tag. 
            Note: only sprites registered with the same Window are checked.
        '''
        from pycat.collision import is_aabb_collision
        for s in self._window.get_sprites_with_tag(tag):
            if is_aabb_collision(self, s):
                return True
        return False        

    def point_toward_mouse_cursor(self):
        self._sprite.rotation = get_rotation_in_degrees_to_point_towards(self.position, self._window.mouse_position)
