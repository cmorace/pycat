from pyglet.clock import schedule_interval as pyglet_schedule_interval
from pyglet.clock import schedule_once as pyglet_schedule_once
from pyglet.clock import unschedule as pyglet_unschedule
from typing import Callable


class Scheduler:
    def __init__(self):
        self.__update_dt: float = 0

    # set by user by calling wait method
    def __user_wait_function(self):
        pass

    # set by user by calling update method
    def __user_update_function(self):
        pass

    @property
    def dt(self) -> float:
        """gets the change in time since the last update

        Returns:
            float: the change in time since the last update
        """
        return self.__update_dt

    def wait(self, time_interval: float, wait_function: Callable[[], None]):
        self.__user_wait_function = wait_function
        pyglet_schedule_once(self.__wait_function, time_interval)

    def update(
        self,
        update_function: Callable[[], None],
        update_interval_time: float = 1 / 120.0,
    ):
        self.__user_update_function = update_function
        pyglet_schedule_interval(self.__update_function, update_interval_time)

    def cancel_update(self):
        pyglet_unschedule(self.__update_function)

    def __wait_function(self, dt: float):
        self.__user_wait_function()

    def __update_function(self, dt: float):
        self.__update_dt = dt
        self.__user_update_function()
