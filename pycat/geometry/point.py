class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def scale(self, w: float):
        self.x *= w
        self.y *= w

    def translate(self, x: float, y: float):
        self.x += x
        self.y += y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        return str(self.x)+','+str(self.y)
