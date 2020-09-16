"""Interface for listening for window events."""
from pycat.base.event.key_event import KeyEvent
from pycat.base.event.mouse_event import MouseEvent


class WindowEventListener():
    """Interface for subscribing to window events.
    
    Override these methods in subclass if needed, then use 
    `window.add_window_event_listener()` to get callbacks"""

    def on_key_press(self, key_event: KeyEvent):
        pass

    def on_key_release(self, key_event: KeyEvent):
        pass

    def on_mouse_drag(self, mouse_event: MouseEvent):
        pass

    def on_mouse_enter(self, mouse_event: MouseEvent):
        pass

    def on_mouse_leave(self, mouse_event: MouseEvent):
        pass

    def on_mouse_motion(self, mouse_event: MouseEvent):
        pass

    def on_mouse_press(self, mouse_event: MouseEvent):
        pass

    def on_mouse_release(self, mouse_event: MouseEvent):
        pass

    def on_mouse_scroll(self, mouse_event: MouseEvent):
        pass