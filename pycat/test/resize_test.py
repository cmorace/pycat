from math import cos, pi, sin

from pycat.base.gl import set_sharp_pixel_scaling
from pycat.core import Color, Sprite, Window
from pycat.geometry.point import Point

w = Window(width=800, height=600)


class ResizeColorSprite(Sprite):

    def on_create(self):
        self.time = 0
        self.color = Color.MAGENTA
        self.position = w.center

    def on_update(self, dt):
        self.rotation += 1
        self.time += dt
        self.width = 200 * sin(self.time/2)
        self.height = 200 * cos(2*pi*sin(self.time/10))

    def on_left_click(self):
        self.set_random_color()


class SharpPixelSprite(Sprite):

    def on_create(self):
        self.image = "img/pixelish.png"
        self.position = Point(self.width, self.height)/2

s = w.create_sprite(position=w.center, color=Color.AZURE)
s.scale_to_width(w.width)
s = w.create_sprite(position=w.center, color=Color.CHARTREUSE)
s.scale_to_height(w.height)
s = w.create_sprite(SharpPixelSprite)
s.scale = 5
s.position = Point(s.width, s.height)/2
w.create_sprite(SharpPixelSprite)
w.create_sprite(ResizeColorSprite)

set_sharp_pixel_scaling(True)
w.run()
