from pycat.core import Window, Sprite
from random import randint

window = Window()


class ColorSprite(Sprite):

    def on_create(self):
        self.goto_random_position()
        self.color = (randint(0, 255) for i in range(3))
        self.opacity = randint(100, 200)
        self.scale_x = randint(50, 200)
        self.scale_y = randint(50, 200)


for _ in range(200):
    window.create_sprite(ColorSprite)


window.run()
