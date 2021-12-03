from typing import List, Optional, Set, Tuple, Union

from pyglet.text import Label as PygletLabel
from pyglet.graphics import OrderedGroup
from pycat.geometry.point import Point

from pycat.base import Color


class Label:
    def __init__(self,
                 text: str = '',
                 x: float = 0,
                 y: float = 0,
                 layer: int = 1,
                 font_size: int = 20,
                 tags: List[str] = []):

        self._label = PygletLabel(text, x=x, y=y, group=OrderedGroup(layer))
        self._label.anchor_x = 'left' # modifying this seems to cause the label to not be rendered
        self._label.anchor_y = 'top' # top, center, and bottom are all valid, but not recommended to change
        self._label.font_size = font_size
        self.__layer = layer
        self.__is_deleted = False
        self.__tags = tags
        # width must be set to support multiline
        self._label.width = 10000
        self._label.multiline = True
        self.is_visible = True

    @property
    def x(self) -> float:
        return self._label.x

    @x.setter
    def x(self, new_x: float):
        self._label.x = new_x

    @property
    def y(self) -> float:
        return self._label.y

    @y.setter
    def y(self, new_y: float):
        self._label.y = new_y

    @property
    def position(self) -> Point:
        """The position (x,y) of the label's top-left corner. Note: changing the anchor properties may effect this."""
        return Point(self._label.x, self._label.y)

    @position.setter
    def position(self, p: Union[Point, Tuple[float, float]]):
        if isinstance(p, Point):
            self._label.x = p.x
            self._label.y = p.y
        else:
            self._label.x, self._label.y = p

    @property
    def text(self) -> str:
        return self._label.text

    @text.setter
    def text(self, new_text: str):
        self._label.text = new_text

    @property
    def font_size(self) -> int:
        return self._label.font_size

    @font_size.setter
    def font_size(self, font_size: int):
        self._label.font_size = font_size

    @property
    def font(self) -> str:
        return self._label.font_name

    @font.setter
    def font(self, file_name):
        self._label.font_name = file_name

    @property
    def color(self) -> Color.RGB:
        return Color.RGB(*self._label.color[:3])

    @color.setter
    def color(self, color: Color.RGB):
        self._label.color = (*color, self._label.color[3])

    @property
    def opacity(self) -> int:
        return self._label.color[3]

    @opacity.setter
    def opacity(self, value: int):
        self._label.color = (*self._label.color[:3], value)

    @property
    def content_width(self):
        return self._label.content_width

    @property
    def content_height(self):
        return self._label.content_height

    @property
    def layer(self) -> int:
        return self.__layer

    @layer.setter
    def layer(self, layer: int):
        self.__layer = layer
        self._label._init_groups(OrderedGroup(layer))

    @property
    def tags(self):
        return self.__tags

    @property
    def is_deleted(self) -> bool:
        return self.__is_deleted

    def delete(self):
        self.__is_deleted = True

    # def contains_point(self, p: Point) -> bool:
    #     """@todo"""
    #     return False

    # def on_click(self, e: MouseEvent):
    #     pass

    # def on_left_click(self):
    #     pass

    def limit_position_to_area(
            self,
            min_x: float,
            max_x: float,
            min_y: float,
            max_y: float
            ):
        """Restrict the label's position to a rectangular region."""
        half_width = self.content_width / 2
        half_height = self.content_height / 2
        center_x = self.x + half_width
        center_y = self.y - half_height
        if center_x < min_x:
            self.x = min_x - half_width
        elif center_x > max_x:
            self.x = max_x - half_width
        if center_y < min_y:
            self.y = min_y + half_height
        elif center_y > max_y:
            self.y = max_y + half_height

    def on_create(self):
        pass

    def on_update(self, dt: float):
        pass

    def draw(self):
        if self.is_visible:
            self._label.draw()
