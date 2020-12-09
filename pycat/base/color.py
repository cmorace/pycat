from random import randint


class Color:

    class RGB(tuple):
        """A tuple of 3 color properties, `red`, `blue`, and `green`.

        This class is an immutable type.
        The red, blue, and green properties are read-only.
        """

        def __new__(cls, red: int, green: int, blue: int):
            return tuple.__new__(cls, (red, green, blue))

        @property
        def red(self):
            return self[0]

        @property
        def green(self):
            return self[1]

        @property
        def blue(self):
            return self[2]

    WHITE = RGB(255, 255, 255)
    BLACK = RGB(0, 0, 0)

    RED = RGB(243, 30, 33)
    GREEN = RGB(94, 170, 43)
    BLUE = RGB(52, 44, 253)
    ORANGE = RGB(241, 144, 25)
    YELLOW = RGB(248, 255, 49)
    PURPLE = RGB(122, 0, 166)
    VERMILION = RGB(242, 72, 29)
    AMBER = RGB(241, 182, 24)
    CHARTREUSE = RGB(199, 235, 41)
    TEAL = RGB(48, 133, 198)
    VIOLET = RGB(60, 235, 153)
    MAGENTA = RGB(151, 18, 68)
    CYAN = RGB(71, 255, 253)
    AZURE = RGB(55, 108, 254)
    ROSE = RGB(245, 0, 119)

    @staticmethod
    def random_rgb():
        red = randint(50, 255)
        green = randint(50, 255)
        blue = randint(50, 255)
        return Color.RGB(red, green, blue)
