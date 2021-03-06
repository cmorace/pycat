"""The point module implements a simple 2-dimensional Point class."""

import math


class Point():
    __slots__ = ['x', 'y']

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def set(self, x: float, y: float):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scale: float) -> 'Point':
        return Point(self.x * scale, self.y * scale)

    def __rmul__(self, scale: float) -> 'Point':
        return Point(self.x * scale, self.y * scale)

    def __truediv__(self, denom: float) -> 'Point':
        return Point(self.x / denom, self.y / denom)

    def __neg__(self) -> 'Point':
        return Point(-self.x, -self.y)

    def __str__(self):
        return str(self.x) + "," + str(self.y)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            self.x = self.x / mag
            self.y = self.y / mag

    def normalized(self) -> 'Point':
        mag = self.magnitude()
        if mag == 0:
            return Point()
        else:
            return Point(self.x / mag, self.y / mag)
