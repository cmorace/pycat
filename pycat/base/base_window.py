"""The base_window module implements the BaseWindow class."""

from typing import Callable, List, Union

from pycat.base.event.window_event_subscriber import WindowEventSubscriber
from pycat.base.event.window_event_manager import WindowEventManager
from pycat.debug.fps_label import FpsLabel
from pycat.geometry.point import Point
from pycat.scheduler import Scheduler
from pyglet import app
from pyglet.window import Window as PygletWindow


class BaseWindow():
    """A window class responsible for managing window-events.

    Custom draw function and update functions can be set with
    the decorators:
    - `@on_draw`
    - `@on_update`
    """

    def __init__(self,
                 width: int = 1280,
                 height: int = 640,
                 title: str = ""):
        """Create a new window.

        Args:
            width (int, optional): the width in pixels. Defaults to 1280.
            height (int, optional): the height in pixels. Defaults to 640.
            title (str, optional): text displayed in title bar. Defaults to "".
        """
        self._window = PygletWindow(width, height, caption=title)
        self._event_manager = WindowEventManager(self._window)
        # for testing convenience
        self._fps_label = FpsLabel()  # needs to be updated and drawn by user
        self.draw_fps = False

    @property
    def width(self) -> int:
        """Return the width of the window in pixels."""
        size = self._window.get_size()
        return size[0]

    @property
    def height(self) -> int:
        """Return the height of the window in pixels."""
        size = self._window.get_size()
        return size[1]

    @property
    def center(self) -> Point:
        """Return the center point of the window."""
        return Point(self.width, self.height) / 2

    @property
    def mouse_position(self) -> Point:
        """Return the current mouse position."""
        return self._event_manager.mouse_position

    @property
    def mouse_delta(self) -> Point:
        """Return the last change in mouse position."""
        return self._event_manager.mouse_delta

    def is_active_key(self, key: Union[int, str]) -> bool:
        """Check if the latest pressed key is a given character or `KeyCode`.

        If multiple keys are presses at the same time, the active key is the
        most recent key pressed.
        """
        return key == self._event_manager.active_key

    def run(self, **kwargs):
        """Start the application.

        Optional keywords can be set for window event callbacks.
        """
        self.subscribe(**kwargs)
        app.run()

    def exit(self):
        """Close the window and exit the application."""
        app.exit()

    #   Drawing
    # -----------------------------------------------------------------------
    def clear(self):
        """Clear the window's graphics content."""
        self._window.clear()

    def on_update(self, update_function: Callable[..., None]):
        """Schedule an update (game-loop) function."""
        Scheduler.update(update_function)

    def on_draw(self, draw_function: Callable[..., None]):
        """Set the windows draw function.

        Not that only one draw function can be set at a time.
        """
        self._window.on_draw = draw_function

    #   Events
    # -----------------------------------------------------------------------
    def add_event_subscriber(self, subscriber: WindowEventSubscriber):
        """Add a `WindowEventListener` to get callbacks on all window events.

        Remember to remove the event listener when done. References to the
        callback functions will prevent garbage collection.
        """
        self._event_manager.add_window_event_subscriber(subscriber)

    def remove_event_subscriber(self, subscriber: WindowEventSubscriber):
        """Remove a `WindowEventListener`.

        Callbacks will stoped getting events after removal.
        """
        self._event_manager.remove_window_event_subscriber(subscriber)

    def subscribe(self, **kwargs):
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

    def unsubscribe(self, **kwargs):
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
