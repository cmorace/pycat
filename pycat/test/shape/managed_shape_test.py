from pycat.core import Window, Color, Point
from pycat.shape import Arc, BorderedRect, Circle, Line, Rectangle, Triangle

window = Window()
o = Point(0, 0)
a = Point(0, window.height/2)
b = Point(window.width, window.height/2)
c = Point(0, window.height)
d = Point(window.width, 0)

window.create_triangle(a.x, a.y, b.x, b.y, c.x, c.y, Color.VERMILION)
window.create_circle(window.center.x, window.center.y, 200)
window.create_rect(window.center.x, window.center.y, 100, 100, Color.BLUE)
window.create_line(a.x, a.y, b.x, b.y, width=4, color=Color.RED)
window.run()
