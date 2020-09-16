"""The window_event_manager module implements the WindowEventManager class."""

from typing import Callable, Dict, List, Set, Union

from pyglet.window import Window as PygletWindow

from pycat.base.event.key_event import KeyEvent
from pycat.base.event.mouse_event import MouseEvent
from pycat.geometry.point import Point
from pycat.debug.print import print_failure
from pycat.base.event.publisher import Subscriber, Publisher
from pycat.base.event.window_event_listener import WindowEventListener


class WindowEventManager:
    """Manage pyglet window events.

    - Adds support for multiple callbacks on window events.
    - Tracks currently presses keys and mouse position
    """

    def __init__(self, window: PygletWindow):
        """Instantiate new instance of WindowEventManager class.

        :param window: the window whose events are to be managed
        :type window: `pyglet.window.Window`
        """
        self.__mouse_position = Point()
        self.__mouse_delta = Point()
        self.__mouse_scroll_delta = Point()

        self.__active_keys: Set[Union[int, str]] = set()
        self.__active_key: Union[int, str] = ""

        self.__publishers: Dict[str, Publisher] = {
            "on_key_press": Publisher[Callable[[KeyEvent], None]](),
            "on_key_release": Publisher[Callable[[KeyEvent], None]](),

            "on_mouse_drag": Publisher[Callable[[MouseEvent], None]](),
            "on_mouse_enter": Publisher[Callable[[MouseEvent], None]](),
            "on_mouse_leave": Publisher[Callable[[MouseEvent], None]](),
            "on_mouse_motion": Publisher[Callable[[MouseEvent], None]](),
            "on_mouse_press": Publisher[Callable[[MouseEvent], None]](),
            "on_mouse_release": Publisher[Callable[[MouseEvent], None]](),
            "on_mouse_scroll": Publisher[Callable[[MouseEvent], None]](),
        }

        window.on_key_press = self.__on_key_press
        window.on_key_release = self.__on_key_release

        window.on_mouse_drag = self.__on_mouse_drag
        window.on_mouse_enter = self.__on_mouse_enter
        window.on_mouse_leave = self.__on_mouse_leave
        window.on_mouse_motion = self.__on_mouse_motion
        window.on_mouse_press = self.__on_mouse_press
        window.on_mouse_release = self.__on_mouse_release
        window.on_mouse_scroll = self.__on_mouse_scroll

    @property
    def mouse_position(self) -> Point:
        """Return the current mouse position.

        If the mouse has exited the window,
        will return the last mouse position before exiting
        :return: the current mouse position
        :rtype: Point
        """
        return self.__mouse_position

    @property
    def active_key(self) -> Union[int, str]:
        return self.__active_key

    @property
    def active_keys(self) -> Set[Union[int,str]]:
        """Return a set of the currently pressed keys.

        Key codes constants are defined in `pycat.keyboard.KEY`
        :return: set of currently pressed keys
        :rtype: Set[int]
        """
        return self.__active_keys

    def add_window_event_listener(self, l: WindowEventListener):
        self.__publishers["on_key_press"].add_subscriber(l.on_key_press)
        self.__publishers["on_key_release"].add_subscriber(l.on_key_release)
        self.__publishers["on_mouse_drag"].add_subscriber(l.on_mouse_drag)
        self.__publishers["on_mouse_enter"].add_subscriber(l.on_mouse_enter)
        self.__publishers["on_mouse_leave"].add_subscriber(l.on_mouse_leave)
        self.__publishers["on_mouse_motion"].add_subscriber(l.on_mouse_motion)
        self.__publishers["on_mouse_press"].add_subscriber(l.on_mouse_press)
        self.__publishers["on_mouse_release"].add_subscriber(l.on_mouse_release)
        self.__publishers["on_mouse_scroll"].add_subscriber(l.on_mouse_scroll)


    def remove_window_event_listener(self, l: WindowEventListener):
        self.__publishers["on_key_press"].remove_subscribers(l.on_key_press)
        self.__publishers["on_key_release"].remove_subscribers(l.on_key_release)
        self.__publishers["on_mouse_drag"].remove_subscribers(l.on_mouse_drag)
        self.__publishers["on_mouse_enter"].remove_subscribers(l.on_mouse_enter)
        self.__publishers["on_mouse_leave"].remove_subscribers(l.on_mouse_leave)
        self.__publishers["on_mouse_motion"].remove_subscribers(l.on_mouse_motion)
        self.__publishers["on_mouse_press"].remove_subscribers(l.on_mouse_press)
        self.__publishers["on_mouse_release"].remove_subscribers(l.on_mouse_release)
        self.__publishers["on_mouse_scroll"].remove_subscribers(l.on_mouse_scroll)
 

    def add_subscribers(self, **kwargs: Union[Subscriber, List[Subscriber]]):
        """Add subscribers by event keyword."""
        for key in kwargs:
            if key in self.__publishers:
                self.__publishers[key].add_subscriber(kwargs[key])
            else:
                self.__invalid_event_name(key)
        self.__update_publishers()

    def remove_subscribers(self, **kwargs: Union[Subscriber, List[Subscriber]]):
        """Remove subscribers by event keyword."""
        for key in kwargs:
            if key in self.__publishers:
                self.__publishers[key].remove_subscribers(kwargs[key])
            else:
                self.__invalid_event_name(key)
        self.__update_publishers()


    def __invalid_event_name(self, name: str):
        msg = str(name) + " is an invalid window event name."
        print_failure(msg)
        assert name in self.__publishers  # throw an assertion error

    # Key Events
    # ------------------------------------------------------------------------
    def __on_key_press(self, symbol: int, mod: int):
        e = KeyEvent(symbol, mod)
        if e.character:
            self.__active_key = e.character
        else:
            self.__active_key = e.symbol
        self.__publishers["on_key_press"].publish(e)
        self.__update_publishers()

    def __on_key_release(self, symbol: int, mod: int):
        e = KeyEvent(symbol, mod)
        if e.character == self.__active_key or e.symbol == self.__active_key:
            self.__active_key = ""
        self.__publishers["on_key_release"].publish(e)
        self.__update_publishers()

    # Mouse Events
    # ------------------------------------------------------------------------
    def __on_mouse_drag(self, x: int, y: int, dx: int,dy: int, b: int, m: int):
        self.__mouse_position.set(x, y)
        self.__mouse_delta.set(dx, dy)
        event = MouseEvent(x, y, dx, dy, b, m)
        self.__publishers["on_mouse_drag"].publish(event)
        self.__update_publishers()

    def __on_mouse_enter(self, x: int, y: int):
        self.__mouse_position.set(x, y)
        event = MouseEvent(x, y)
        self.__publishers["on_mouse_enter"].publish(event)
        self.__update_publishers()


    def __on_mouse_leave(self, x: int, y: int):
        self.__mouse_position.set(x, y)
        event = MouseEvent(x, y)
        self.__publishers["on_mouse_leave"].publish(event)
        self.__update_publishers()

    def __on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.__mouse_position.set(x, y)
        self.__mouse_delta.set(dx, dy)
        event = MouseEvent(x, y, dx, dy)
        self.__publishers["on_mouse_motion"].publish(event)
        self.__update_publishers()

    def __on_mouse_press(self, x: int, y: int, b: int, m: int):
        self.__mouse_position.set(x, y)
        event = MouseEvent(x, y, 0, 0, b, m)
        self.__publishers["on_mouse_press"].publish(event)
        self.__update_publishers()

    def __on_mouse_release(self, x: int, y: int, b: int, m: int):
        self.__mouse_position.set(x, y)
        event = MouseEvent(x, y, 0, 0, b, m)
        self.__publishers["on_mouse_release"].publish(event)
        self.__update_publishers()

    def __on_mouse_scroll(self, x: int, y: int, dx: int, dy: int):
        self.__mouse_position.set(x, y)
        self.__mouse_scroll_delta.set(dx, dy)
        event = MouseEvent(x, y, dx, dy)
        self.__publishers["on_mouse_scroll"].publish(event)
        self.__update_publishers()

    def __update_publishers(self):
        for publisher in self.__publishers.values():
            publisher.update()

