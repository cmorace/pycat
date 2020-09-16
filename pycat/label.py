from typing import List
from pyglet.text import Label as PygletLabel
from pycat.geometry.point import Point
from pycat.base.event.mouse_event import MouseEvent


class Label:
    def __init__(self,
                 text: str,
                 x: float = 0,
                 y: float = 0,
                 layer: int = 0,
                 font_size: int = 20,
                 tags: List[str] = []):
        self.__label = PygletLabel(text, x=x, y=y)
        self.__label.font_size = font_size
        self.__layer = layer
        self.__is_deleted = False
        self.__tags = tags

    @property
    def x(self) -> float:
        return self.__label.x

    @x.setter
    def x(self, new_x: float):
        self.__label.x = new_x

    @property
    def y(self) -> float:
        return self.__label.y

    @y.setter
    def y(self, new_y: float):
        self.__label.y = new_y

    @property
    def text(self) -> str:
        return self.__label.text

    @text.setter
    def text(self, new_text: str):
        self.__label.text = new_text

    @property
    def font_size(self) -> int:
        return self.__label.font_size

    @font_size.setter
    def font_size(self, font_size: int):
        self.__label.font_size = font_size

    @property
    def layer(self) -> int:
        return self.__layer

    @layer.setter
    def layer(self, layer: int):
        self.__layer = layer

    @property
    def tags(self):
        return self.__tags

    def is_deleted(self):
        return self.__is_deleted

    def delete(self):
        self._is_deleted = True



    def contains_point(self, p: Point) -> bool:
        """@todo"""
        return False

    def on_click(self, e: MouseEvent):
        pass

    def on_left_click(self):
        pass

    def limit_position_to_area(self, min_x: int, max_x: int, min_y: int, max_y: int):
        pass

    def on_update(self, dt: float):
        pass

    def draw(self):
        self.__label.draw()
