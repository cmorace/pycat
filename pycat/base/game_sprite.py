"""forked from pycat.sprite to do some testing"""
from typing import List
from pycat.base.sprite import Sprite as BaseSprite
from pycat.base.game_window import Window
from pycat.collision import is_aabb_collision
from pycat.base.image import Image

from random import randint

# Question: Suppose a class MySprite inherits from Sprite,
# If it is instantiated s = MySprite(window), it will not be registered
# so it will not be drawn, updated, or receive any events
# maybe we should register the sprite in __init__() to handle this case ?


class Sprite(BaseSprite):
    """A Sprite that is "managed" by a Window. 
        
    Never instantiate this class directly, it may only be created by a Window. 
    The connection to a Window provides additional functionality.
    Primarially:
    - `on_create` is called when the sprite is added to the window
    - `on_update` is scheduled to be called 60 times a second
    - `on_click` is called when the sprite is clicked!
    """
    def __init__(
        self, 
        window: Window,
        tags: List[str] = []     
    ):        
        self._window = window
        super().__init__(tags=tags)
        self.__is_deleted = False


    ################################################################################
    # Override these to set the sprite's behavior
    ################################################################################
    def on_create(self):
        """Called (once) when added to a window."""
        pass

    def on_update(self, dt):
        """Called 60 times a second when added to a window. 
        
        Stops being called when removed from window.
        """
        pass

    def on_click(self, x, y, button, modifiers):
        """Called when ANY mouse button is clicked while the cursor is over this sprite."""
        pass

    def on_left_click(self):
        """Simplified function signature for left clicks only."""
        pass


    ################################################################################
    # The rest
    ################################################################################


    @property
    def window(self) -> Window:
        return self._window 

    @property
    def _is_deleted(self) -> bool:
        return self.__is_deleted 

    def delete(self):
        self.__is_deleted = True

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
        for s in self._window.get_all_sprites():
            if self is not s and is_aabb_collision(self, s):
                return True
        return False             

    def touching_any_sprite_with_tag(self, tag):
        """Checks if this sprite is touching any other sprite with appropiate tag. 
        
        Note: only sprites registered with the same Window are checked.
        """
        for s in self._window.get_sprites_with_tag(tag):
            if is_aabb_collision(self, s):
                return True
        return False        

    def point_toward_mouse_cursor(self):
        self.point_toward(self._window.mouse_position)
