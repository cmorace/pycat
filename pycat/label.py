from pyglet.text import Label as PygletLabel


class Label:
    def __init__(self,
                 text: str,
                 x: float = 0,
                 y: float = 0,
                 font_size: int = 20):
        self.__label = PygletLabel(text, x=x, y=y)
        self.__label.font_size = font_size

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

    def draw(self):
        self.__label.draw()
