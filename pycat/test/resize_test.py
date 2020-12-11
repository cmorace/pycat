from pycat.core import Color, Sprite, Window
from math import sin, cos, pi

w = Window(width=800, height=600, draw_sprite_rects=True)


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


s = w.create_sprite(position=w.center, color=Color.AZURE)
s.scale_to_width(w.width)
s = w.create_sprite(position=w.center, color=Color.CHARTREUSE)
s.scale_to_height(w.height)
w.create_sprite(ResizeColorSprite)

w.run()
