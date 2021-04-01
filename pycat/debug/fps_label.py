""" The fps_label module implements the FpsLabel class"""

from pycat.base.color import Color
from pyglet.clock import get_fps
from pycat.label import Label


class FpsLabel(Label):
    def on_create(self):
        self.__msg = "FPS: "
        self.font_size = 30
        self.color = (255, 0, 255)

    def update(self):
        fps = int(get_fps())
        self.text = self.__msg + str(fps)
        if fps > 40:
            self.color = Color(0, 255, 0)
        elif fps > 30:
            self.color = Color(255, 255, 0)
        else:
            self.color = Color(255, 0, 0)
