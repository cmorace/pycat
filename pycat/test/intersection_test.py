from pycat.base.event.mouse_event import MouseEvent
from pycat.core import Window, Point, Color
from pycat.shape import Circle, Line
from pycat.geometry.intersection import line_intersection

w = Window()


def on_mouse_motion(m: MouseEvent):
    w.clear_drawables()
    a = Point(0, w.height)
    b = m.position
    c = Point(100, 100)
    d = Point(w.width-100, w.height-100)
    w.add_drawable(Line(a, b))
    w.add_drawable(Line(c, d))
    x = line_intersection(a.x, a.y, b.x, b.y, c.x, c.y, d.x, d.y)
    if x:
        w.add_drawable(Circle(x, 10, color=Color.RED))


w.run(on_mouse_motion=on_mouse_motion)
