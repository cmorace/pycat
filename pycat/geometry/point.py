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

    def translate(self, p: 'Point'):
        self.translate(p.x,p.y)
