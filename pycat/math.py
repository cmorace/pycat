from math import pi, sin, cos, sqrt
from .geometry.point import Point


def degree_to_radian(degrees: float) -> float:
    return degrees * pi / 180


def radian_to_degree(radians: float) -> float:
    return radians * 180 / pi


def get_direction_from_degrees(degrees: float) -> Point:
    radians = degree_to_radian(degrees)
    return Point(cos(radians), sin(radians))


def get_distance(a: Point, b: Point) -> float:
    return sqrt(get_square_distance(a, b))


def get_square_distance(a: Point, b: Point) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return dx * dx + dy * dy
