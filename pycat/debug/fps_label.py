""" The fps_label module implements the FpsLabel class"""

from pyglet.clock import get_fps
from pycat.base.label import Label


class FpsLabel(Label):
    def __init__(self, x: float = 5, y: float = 0):
        self.__msg = "FPS: "
        super().__init__(self.__msg, x, y, font_size=30)
        self.color= (255,0,255,255)
        self.background_color = (50, 50, 50, 180)
        self.background_padding = 5
        self.fit_background_to_content()


    def update(self):
        fps = int(get_fps())
        self.text = self.__msg + str(fps)
        if fps > 40:
            self.color = (0, 255, 0, 255)
        elif fps > 30:
            self.color = (255, 255, 0, 255)
        else:
            self.color = (255, 0, 0, 255)
        self.fit_background_to_content()

