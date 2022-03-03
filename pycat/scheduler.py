from inspect import signature
from typing import Callable, Dict

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
    __functions_without_dt = dict()

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
               delay: float = 1/120,
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
            def f(dt): callback()
            Scheduler.__functions_without_dt[callback] = f
            schedule_interval(f, delay)

    @staticmethod
    def soft_update(callback: Callable[..., None],
                    delay: float = 1/120,
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
            def f(dt): callback()
            Scheduler.__functions_without_dt[callback] = f
            schedule_interval_soft(f, delay)

    @staticmethod
    def cancel_update(callback: Callable[..., None]):
        """Cancel updates on a previously scheduled callback."""
        if callback in Scheduler.__functions_without_dt:
            f = Scheduler.__functions_without_dt[callback]
            unschedule(f)
            del Scheduler.__functions_without_dt[callback]
        else:
            unschedule(callback)

    # possible refactor of update
    # can call existing function with params, but no dt, e.g.
    # Scheduler.update_test(window.create_sprite, Gem, delay=1)
    # @staticmethod
    # def update_test(callback: Callable[..., None], *args, delay=1/120):
    #     print(type(args[0]))
    #     schedule_interval(lambda dt, *args: callback(*args), delay, *args)
