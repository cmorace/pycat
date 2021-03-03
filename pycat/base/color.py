from random import randint


class Color(tuple):
    """A tuple of 3 color properties, `red`, `blue`, and `green`.
    Constructor has the form `color = Color(red, green, blue)`.
    The `red`, `green` and `blue` properties should be in the range [0,255].
    This class is an immutable type, properties are read-only.
    """
    class RGB(tuple):

        def __new__(cls, red: int, green: int, blue: int):
            return tuple.__new__(cls, (red, green, blue))

        @property
        def r(self):
            return self[0]

        @property
        def g(self):
            return self[1]

        @property
        def b(self):
            return self[2]

    def __new__(cls, red: int, green: int, blue: int) -> RGB:
        """Constructor."""
        return tuple.__new__(cls, (red, green, blue))

    @property
    def r(self):
        return self[0]

    @property
    def g(self):
        return self[1]

    @property
    def b(self):
        return self[2]

    WHITE = RGB(255, 255, 255)
    BLACK = RGB(0, 0, 0)

    RED = RGB(255, 0, 0)
    GREEN = RGB(0, 255, 0)
    BLUE = RGB(0, 0, 255)
    ORANGE = RGB(241, 144, 25)
    YELLOW = RGB(248, 255, 49)
    PURPLE = RGB(122, 0, 166)
    VERMILION = RGB(242, 72, 29)
    AMBER = RGB(241, 182, 24)
    CHARTREUSE = RGB(199, 235, 41)
    TEAL = RGB(48, 133, 198)
    VIOLET = RGB(127, 0, 255)
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

    @staticmethod
    def get_complement(c: 'Color'):
        red = 255 - c.r
        green = 255 - c.g
        blue = 255 - c.b
        return Color.RGB(red, green, blue)
