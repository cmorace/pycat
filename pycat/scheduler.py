from inspect import signature
from typing import Callable

from pyglet.clock import (schedule_interval, schedule_interval_soft,
                          schedule_once, unschedule)


class Scheduler:
    """Implements static methods for scheduling callback functions.

    You must pass a callback function as a parameter to these methods.
    If the callback takes arguments, the first argument must be a float.
    When the function is called its first argument will have the actual
    delay time as its value.
    Note: The default time function used is `time.perf_counter()`
    """
    @staticmethod
    def wait(delay: float, callback: Callable[..., None], *args, **kwargs):
        """Wait for delay time then call a scheduled callback function.

        If `callback` takes arguments then the first argument must be a
        float which will get the value of the actual delay time.
        """
        if len(signature(callback).parameters):
            schedule_once(callback, delay, *args, **kwargs)
        else:
            schedule_once(lambda dt: callback(), delay)

    @staticmethod
    def update(callback: Callable[..., None],
               delay: float = 1 / 70,
               *args,
               **kwargs):
        """Update a scheduled callback function at regular delay time interval.

        If `callable` takes arguments then the first argument must be a
        float which will get the value of the actual delay time since the
        previous update.
        """
        if len(signature(callback).parameters):
            schedule_interval(callback, delay, *args, **kwargs)
        else:
            schedule_interval(lambda dt: callback(), delay)

    @staticmethod
    def soft_update(callback: Callable[..., None],
                    delay: float = 1 / 70,
                    *args,
                    **kwargs):
        """Update a scheduled callback function at regular delay time interval.

        If `callable` takes arguments then the first argument must be a
        float which will get the value of the actual delay time since the
        previous update.
        """
        if len(signature(callback).parameters):
            schedule_interval_soft(callback, delay, *args, **kwargs)
        else:
            schedule_interval_soft(lambda dt: callback(), delay)

    @staticmethod
    def cancel_update(callback: Callable[..., None]):
        """Cancel updates on a previously scheduled callback."""
        unschedule(callback)
