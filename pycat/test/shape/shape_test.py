from pycat.core import Window, Color, Point
from pycat.shape import Arc, BorderedRect, Circle, Line, Rectangle, Triangle

window = Window()
o = Point(0, 0)
a = Point(0, window.height/2)
b = Point(window.width, window.height/2)
c = Point(0, window.height)
d = Point(window.width, 0)

window.add_drawable(Triangle(a, b, c, color=Color.AZURE))
window.add_drawable(Triangle(o, b, d, color=Color.VERMILION))
window.add_drawable(Circle(window.center, 200))
window.add_drawable(Line(a, b, width=4, color=Color.RED))
window.add_drawable(Arc(window.center, 150, 1.5705, color=Color.AZURE))
window.add_drawable(BorderedRect(window.center, 150, 200, 10,
                                 fill_color=Color.TEAL,
                                 border_color=Color.AMBER))
window.add_drawable(Rectangle(window.center, 100, 100, color=Color.VIOLET))
window.run()
