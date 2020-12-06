from random import randint

from pycat.base.event.mouse_event import MouseEvent
from pycat.base.base_sprite import BaseSprite
from pycat.collision import is_rotated_box_collision


class Sprite(BaseSprite):
    """A Sprite that is "managed" by a Window.

    Never instantiate this class directly, it may only be created by a Window.
    The connection to a Window provides additional functionality.
    Primarially:
    - `on_create` is called when the sprite is added to the window
    - `on_update` is scheduled to be called 60 times a second
    - `on_click` is called when the sprite is clicked!
    """

    def __init__(self, window):
        self._window = window
        super().__init__()
        self.__is_deleted = False

    ##################################################################
    # Override these to set the sprite's behavior
    ##################################################################

    def on_create(self):
        """Called (once) when added to a window."""
        pass

    def on_update(self, dt):
        """Called 60 times a second when added to a window.

        Stops being called when removed from window.
        """
        pass

    def on_click(self, mouse_event: MouseEvent):
        """Called when ANY mouse button is clicked on this sprite."""
        pass

    def on_left_click(self):
        """Simplified function signature for left clicks only."""
        pass

    ##################################################################
    # The rest
    ##################################################################

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        self.window = window

    @property
    def is_deleted(self) -> bool:
        return self.__is_deleted

    def delete(self):
        self.__is_deleted = True

    def goto_random_position(self):
        self.x = randint(0, self._window.width)
        self.y = randint(0, self._window.height)

    def touching_window_edge(self) -> bool:
        return (self.x <= 0 or self.x >= self._window.width or self.y <= 0
                or self.y >= self._window.height)

    def touching_any_sprite(self):
        if not self.is_visible:
            return False
        for s in self._window.get_all_sprites():
            if s is not self and s.is_visible and is_rotated_box_collision(self, s):
                return True
        return False

    def touching_any_sprite_with_tag(self, tag: str):
        """Checks if sprite is touching any other sprite with appropiate tag.
        """
        if not self.is_visible:
            return False
        for s in self._window.get_sprites_with_tag(tag):
            if s is not self and s.is_visible and is_rotated_box_collision(self, s):
                return True
        return False

    def point_toward_mouse_cursor(self):
        """Rotate to point towards mouse position."""
        self.point_toward(self._window.mouse_position)
