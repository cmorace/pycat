from pycat.core import Window, Color, Point
from pycat.shape import Arc, BorderedRect

window = Window()
o = Point(0, 0)
a = Point(0, window.height/2)
b = Point(window.width, window.height/2)
c = Point(0, window.height)
d = Point(window.width, 0)

tri1 = window.create_triangle(a, b, c, color=Color.AZURE)
tri2 = window.create_triangle(o, b, d, color=Color.VERMILION)
circle = window.create_circle(radius=200)
line = window.create_line(a, b, width=4, color=Color.RED)

arc = Arc(window.center, radius=150, angle=1.5705, color=Color.AZURE)
window.add_drawable(arc)

bordered_rect = BorderedRect(window.center, 150, 200, 10,
                             fill_color=Color.TEAL, border_color=Color.AMBER)
window.add_drawable(bordered_rect)

rect = window.create_rect(window.center, 100, 100, color=Color.VIOLET)


window.run()
