from typing import List

from pyglet import shapes


from pycat.base.color import Color
from pycat.geometry import Point


class Line(shapes.Line):

    def __init__(
        self,
        a: Point,
        b: Point,
        width: float = 1,
        color: Color = Color.WHITE
    ):
        super().__init__(x=a.x,
                         y=a.y,
                         x2=b.x,
                         y2=b.y,
                         width=width,
                         color=color)


class Triangle(shapes.Triangle):

    def __init__(
        self,
        a: Point,
        b: Point,
        c: Point,
        color: Color = Color.WHITE
    ):
        super().__init__(x=a.x,
                         y=a.y,
                         x2=b.x,
                         y2=b.y,
                         x3=c.x,
                         y3=c.y,
                         color=color)

    def get_points(self) -> List[Point]:
        return [Point(self.x, self.y),
                Point(self.x2, self.y2),
                Point(self.x3, self.y3)]


class Circle(shapes.Circle):

    def __init__(
        self,
        center: Point,
        radius: float,
        segments: int = None,
        color: Color = Color.WHITE
    ):
        super().__init__(x=center.x,
                         y=center.y,
                         radius=radius,
                         segments=segments,
                         color=color)

    @property
    def center(self) -> Point:
        return Point(self.x, self.y)

    @center.setter
    def center(self, point: Point):
        self.x = point.x
        self.y = point.y


class Rectangle(shapes.Rectangle):

    def __init__(
        self,
        center: Point,
        width: float,
        height: float,
        color: Color = Color.WHITE
    ):
        super().__init__(x=center.x,
                         y=center.y,
                         width=width,
                         height=height,
                         color=color)


class Arc(shapes.Arc):

    def __init__(
        self,
        center: Point,
        radius: float,
        segments: int = None,
        angle: float = shapes.math.tau,
        start_angle: float = 0,
        is_closed: bool = False,
        color: Color = Color.WHITE
    ):
        super().__init__(x=center.x,
                         y=center.y,
                         radius=radius,
                         segments=segments,
                         angle=angle,
                         start_angle=start_angle,
                         closed=is_closed,
                         color=color)


class BorderedRect(shapes.BorderedRectangle):
    def __init__(
        self,
        center: Point,
        width: float,
        height: float,
        border_width: float,
        fill_color: Color = Color.WHITE,
        border_color: Color = Color.CYAN
    ):
        super().__init__(x=center.x,
                         y=center.y,
                         width=width,
                         height=height,
                         border=border_width,
                         color=fill_color,
                         border_color=border_color)


class Polyline():

    def __init__(
        self,
        points: List[Point],
        width: float = 1,
        color: Color = Color.CYAN,
        is_closed: bool = False
    ):
        # todo: triangulate line segments' joints
        self.lines = [Line(points[i], points[i+1], width, color)
                      for i in range(len(points)-1)]
        self.is_closed = is_closed
        if is_closed:
            self.lines.append(Line(points[0], points[-1], width, color))

    def draw(self):
        for line in self.lines:
            line.draw()


class Polygon():
    def __init__(self, points: List[Point], is_wireframe: bool = False):

        # triangle failed to install on a student's home pc
        # making it an optional dependency until we find a solution
        from triangle import triangulate
        from numpy import array

        self.boundary_array = array([[p.x, p.y] for p in points])
        self.is_wireframe = is_wireframe

        segments = [[i, i+1] for i in range(len(self.boundary_array))]
        segments.append([0, len(self.boundary_array) - 1])
        self.complex = triangulate({'vertices': self.boundary_array,
                                    'segments': array(segments)}, 'p q')

        points = [Point(v[0], v[1]) for v in self.complex['vertices']]
        self.mesh = [Triangle(points[t[0]], points[t[1]], points[t[2]])
                     for t in self.complex['triangles']]

        if is_wireframe:
            self.wireframe = [
                Polyline(tri.get_points(), is_closed=True, color=Color.BLACK)
                for tri in self.mesh]

    def draw(self):
        for triangle in self.mesh:
            triangle.draw()

        if self.is_wireframe:
            for wire in self.wireframe:
                wire.draw()
