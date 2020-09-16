"""The window module implements the Window class."""

from typing import Callable, Union

from pycat.base.event.window_event_listener import WindowEventListener
from pycat.base.event.window_event_manager import WindowEventManager
from pycat.debug.fps_label import FpsLabel
from pycat.geometry.point import Point
from pycat.scheduler import Scheduler
from pyglet import app
from pyglet.window import Window as PygletWindow


class Window():

    def __init__(self,
                 width: int = 1280,
                 height: int = 640,
                 title: str = ""):

        self._window = PygletWindow(width, height, caption = title)
        self._event_manager = WindowEventManager(self._window)
        # for testing convenience
        self._fps_label = FpsLabel() # needs to be updated and drawn by user

    @property
    def width(self) -> int:
        """The width of the window in pixels."""
        size = self._window.get_size()
        return size[0]

    @property
    def height(self) -> int:
        """The height of the window in pixels."""
        size = self._window.get_size()
        return size[1]

    @property
    def mouse_position(self) -> Point:
        """The current mouse position."""
        return self._event_manager.mouse_position

    @property
    def mouse_delta(self) -> Point:
        """The current mouse position."""
        return self._event_manager.__mouse_delta

    @property
    def center(self) -> Point:
        """The center of the window."""
        return Point(self.width, self.height) / 2

    def is_active_key(self, key: Union[int, str]) -> bool:
        """Checks if the latest pressed key is a given character or `KeyCode`.
        
        If multiple keys are pressed at the same time, the active key is the
        most recent key to be pressed."""
        return key == self._event_manager.active_key

    def run(self, **kwargs):
        """Starts the application.

        Optional keywords can be set for window event callbacks.
        """
        self.add_event_listeners(**kwargs)
        app.run()

    def exit(self):
        """Close the window and exit the application."""
        app.exit()

    #   Drawing
    # -----------------------------------------------------------------------

    def clear(self):
        """Clears the window's graphics content."""
        self._window.clear()

    def on_update(self, update_function: Callable[..., None]):
        """Convenience method to schedule an update function."""
        Scheduler.update(update_function)

    def on_draw(self, draw_function: Callable[..., None]):
        """Sets the windows draw function.

        Not that only one draw function can be set at a time.
        """
        self._window.on_draw = draw_function


    #   Events
    # -----------------------------------------------------------------------
    def add_window_event_listener(self, l: WindowEventListener):
        """Add a `WindowEventListener` to get callbacks on all window events.

        Remember to remove the event listener when done. References to the
        callback functions will prevent an object from being removed from memory.
        """
        self._event_manager.add_window_event_listener(l)

    def remove_window_event_listener(self, l: WindowEventListener):
        """Removes a `WindowEventListener`.
        
        Callbacks will stoped getting events after removal.
        """
        self._event_manager.remove_window_event_listener(l)

    def add_event_listeners(self, **kwargs):
        """Add multiple callback functions for window events.
        
        To add callbacks use the window event name as a keyword
        followed by the callback function or list of callback functions
        e.g. 
        - `on_key_press=my_key_press`
        - `on_mouse_drag=[my_mouse_drag, my_other_mouse_drag]`
        
        callback functions should take a single `KeyEvent` or `MouseEvent`
        argument.

        Accepted Keyword Arguments:

        - `on_key_press`
        - `on_key_release`
        - `on_mouse_drag`
        - `on_mouse_enter`
        - `on_mouse_leave`
        - `on_mouse_motion`
        - `on_mouse_press`
        - `on_mouse_release`
        - `on_mouse_scroll`
        """
        self._event_manager.add_subscribers(**kwargs)

    def remove_event_listeners(self, **kwargs):
        """Remove multiple callback functions for window events.
        
        Only callback functions that have been previously added should
        be removed. If callback functions are not removed then the
        object will not be collected by the garbage collector.

        To remove callbacks use the window event name as a keyword
        followed by the callback function or list of callback functions
        e.g. 
        - `on_key_press=my_key_press`
        - `on_mouse_drag=[my_mouse_drag, my_other_mouse_drag]`
        
        callback functions should take a single `KeyEvent` or `MouseEvent`
        argument.

        Accepted Keyword Arguments:

        - `on_key_press`
        - `on_key_release`
        - `on_mouse_drag`
        - `on_mouse_enter`
        - `on_mouse_leave`
        - `on_mouse_motion`
        - `on_mouse_press`
        - `on_mouse_release`
        - `on_mouse_scroll`

        """

        self._event_manager.remove_subscribers(**kwargs)
