from pycat.core import Window, Point
from pycat.math import get_direction_from_degrees

window = Window()
a = Point(window.width / 2, 0)
b = Point(a.x, 0.35 * window.height)
branch = window.create_line(a, b, width=2)


def make_tree(
    a: Point,
    rotation: float = 90,
    length: float = 100,
    height: int = 8,
    dr: float = 70,
    ds: float = 0.6275
):
    if height > 0:

        b1 = a + length * get_direction_from_degrees(rotation+dr)
        window.create_line(a, b1, width=2)
        make_tree(b1, rotation+dr, length*ds, height-1)

        b2 = a + length * get_direction_from_degrees(rotation-dr)
        window.create_line(a, b2, width=2)
        make_tree(b2, rotation-dr, length*ds, height-1)


make_tree(b, length=b.y)
window.run()
