from pycat.core import Window, Color
from pycat.geometry import Point
from pycat.shape import Polygon, Polyline
from math import cos, sin
from random import uniform

w = Window()

points = []
n = 40
for i in range(n):
    theta = i * 6.28/n
    x = uniform(200, 300) * cos(theta) + w.center.x
    y = uniform(200, 300) * sin(theta) + w.center.y
    points.append(Point(x, y))

w.add_drawable(Polygon(points, is_wireframe=True))
w.add_drawable(Polyline(points, width=3, color=Color.CYAN, is_closed=True))

w.run()
