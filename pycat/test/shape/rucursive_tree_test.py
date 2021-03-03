from pycat.core import Window, Point
from pycat.math import get_direction_from_degrees

window = Window()
x, y1, y2 = window.width / 2, 0, 0.35 * window.height
branch = window.create_line(x, y1, x, y2, width=2)


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
        window.create_line(a.x, a.y, b1.x, b1.y, width=2)
        make_tree(b1, rotation+dr, length*ds, height-1)

        b2 = a + length * get_direction_from_degrees(rotation-dr)
        window.create_line(a.x, a.y, b2.x, b2.y, width=2)
        make_tree(b2, rotation-dr, length*ds, height-1)


make_tree(Point(branch.x2, branch.y2), length=branch.y2)
window.run()
