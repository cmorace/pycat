from math import atan2, cos, pi, sin, sqrt
from pycat.geometry.point import Point


def degree_to_radian(degrees: float) -> float:
    return degrees * pi / 180


def radian_to_degree(radians: float) -> float:
    return radians * 180 / pi


def get_distance(a: Point, b: Point) -> float:
    return sqrt(get_square_distance(a, b))


def get_square_distance(a: Point, b: Point) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return dx * dx + dy * dy


def get_direction_from_degrees(degrees: float) -> Point:
    radians = degree_to_radian(degrees)
    return Point(cos(radians), sin(radians))


def get_degrees_from_direction(direction: Point) -> float:
    return radian_to_degree(atan2(direction.y, direction.x))


def get_rotated_point(p: Point, degrees: float):
    r = degree_to_radian(degrees)
    cr = cos(r)
    sr = sin(r)
    return Point(p.x * cr - p.y * sr, p.x * sr + p.y * cr)


def dot(p: Point, q: Point) -> float:
    return p.x*q.x + p.y*q.y


def project_p_onto_q(p: Point, q: Point):
    return (dot(p, q)/dot(q, q)) * q
