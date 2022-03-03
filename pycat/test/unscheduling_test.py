from pycat.core import Window, Scheduler
count = 10
w = Window()
label = w.create_label(text=str(count), font_size=50)


def test_no_param():
    global count
    count -= 1
    if count == 0:
        Scheduler.cancel_update(test_no_param)
    label.text = str(count)


Scheduler.update(test_no_param, delay=0.2)
w.run()
