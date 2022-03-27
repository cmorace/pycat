from pycat.core import Sprite, Color

class Turtle(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_pen_down: bool = True
        self._pen_width: float = 1
        self._pen_color: Color = Color.GREEN


    @property
    def is_pen_down(self) -> bool:
        return self._is_pen_down

    def pen_down(self):
        self._is_pen_down = True

    def pen_up(self):
        self._is_pen_down = False


    @property
    def pen_width(self) -> float:
        return self._pen_width

    @pen_width.setter
    def pen_width(self, width: float):
        self._pen_width = width


    @property
    def pen_color(self) -> Color:
        return self._pen_color    

    @pen_color.setter
    def pen_color(self, color: Color):
        self._pen_color = color


    def turn_right(self, degrees: float):
        self.rotation -= degrees

    def turn_left(self, degrees: float):
        self.rotation += degrees

    def move_forward(self, distance: float):
        prev_x = self.x
        prev_y = self.y
        super().move_forward(distance)
        if self._is_pen_down:
            self.window.create_line(prev_x, prev_y, self.x, self.y, 
                width = self._pen_width, color = self._pen_color)