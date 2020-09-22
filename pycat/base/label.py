"""The label module implements the Label class"""
from typing import Tuple, Optional
from pyglet.text import Label as PygletLabel

from pycat.base.base_sprite import BaseSprite
from pycat.base.image import Image


class Label:
    def __init__(self,
                 text: str,
                 x: float = 0,
                 y: float = 0,
                 font_size: int = 20,
                 width: int = 500,
                 height: Optional[int] = None,
                 layer: int = 0,
                 align: str = "left",
                 font_name: Optional[str] = None):

        self._label = PygletLabel(text,
                                  x=x,
                                  y=y,
                                  font_size=font_size,
                                  font_name=font_name,
                                  width=width,
                                  height=height,
                                  anchor_x="left",
                                  anchor_y="bottom",
                                  align=align,
                                  multiline=True)

        self.background_padding = 0
        self._background: Optional[BaseSprite] = None
        self._layer = layer
        self.__align = align

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
    def color(self) -> Tuple[int, int, int, int]:
        return self._label.color

    @color.setter
    def color(self, color: Tuple[int, int, int, int]):
        self._label.color = color

    @property
    def layer(self) -> int:
        return self._layer

    @layer.setter
    def layer(self, layer: int):
        self._layer = layer

    @property
    def background_color(self) -> Optional[Tuple[int, int, int, int]]:
        if self._background is None:
            return None
        else:
            r = self._background.color[0]
            g = self._background.color[1]
            b = self._background.color[2]
            a = self._background.opacity
            return (r, g, b, a)

    @background_color.setter
    def background_color(self, color: Tuple[int, int, int, int]):
        image = Image.get_solid_color_texture(1, 1, color)
        image.anchor_x = 0
        image.anchor_y = 0
        self._background = BaseSprite(image, self.x, self.y)
        self.fit_background_to_content()

    def fit_background_to_content(self):
        pad = 2 * self.background_padding
        self._background.scale_x = self._label.content_width + pad
        self._background.scale_y = self._label.content_height + pad
        if self.__align == "left":
            self._background.x = self.x - self.background_padding
            self._background.y = self.y - self.background_padding
        elif self.__align == "center":
            dx = (self._label.width - self._label.content_width) / 2
            self._background.x = self.x + dx - self.background_padding
            self._background.y = self.y - self.background_padding
        elif self.__align == "right":
            dx = self._label.width - self._label.content_width
            self._background.x = self.x + dx - self.background_padding
            self._background.y = self.y - self.background_padding

    def draw(self):
        if self._background is not None:
            self._background.draw()
        self._label.draw()
