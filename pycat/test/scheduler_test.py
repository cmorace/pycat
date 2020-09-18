from pycat.base.window import Window
from pycat.scheduler import Scheduler

window = Window(80, 20)


def test_soft_update(delay, times):
    times.append(delay)


def test_update(delay, times):
    times.append(delay)


def cancel_updates(delay, update_times, soft_update_times):
    Scheduler.cancel_update(test_update)
    Scheduler.cancel_update(test_soft_update)
    n1 = len(update_times)
    n2 = len(soft_update_times)
    print(n1, n2)
    for i in range(min(n1, n2)):
        print(update_times[i])
        print(soft_update_times[i])
        print("----------------------")
    window.exit()


def start_test_update(delay, arg):
    print("start_test_update(delay, keyword)")
    print("delay =", delay)
    arg.append(round(delay, 3))
    print(arg)
    print("=============================================")
    update_times = []
    soft_update_times = []
    delta_time = 1/80
    Scheduler.update(test_update, delta_time, update_times)
    Scheduler.update(test_soft_update, delta_time, soft_update_times)
    Scheduler.wait(2, cancel_updates, update_times, soft_update_times)


def test_wait_with_args(delay, arg):
    print("test_wait_with_args(delay, arg, keyword)")
    print("delay =", delay)
    arg.append(round(delay, 3))
    print("=============================================")
    Scheduler.wait(1, start_test_update, arg)


def test_wait(delay):
    print("test_wait(delay) called")
    print("delay =", delay)
    print("=============================================")
    Scheduler.wait(1, test_wait_with_args, [round(delay, 3)])


def test_wait_no_args():
    print("test_wait_no_args() called")
    print("=============================================")
    Scheduler.wait(1, test_wait)


Scheduler.wait(1, test_wait_no_args)


window.run()
