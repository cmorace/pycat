
from pycat.core import Window, Label, Scheduler

w = Window(enforce_window_limits=False)


class TestLabel(Label):
    def on_create(self):
        self.font_size = 40
        self.text = "hello world"
        self.y = w.height
        self.x = (w.width - self.content_width) / 2

    def on_update(self, dt: float):
        if self.y < 100:
            self.delete()
        else:
            self.y -= 10


num_labels = 0


def spawn_label(dt):
    w.create_label(TestLabel)
    global num_labels
    num_labels += 1
    if num_labels == 10:
        Scheduler.cancel_update(spawn_label)


Scheduler.update(spawn_label, delay=1)

w.run()
