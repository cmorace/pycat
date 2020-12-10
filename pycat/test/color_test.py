from random import randint

from pycat.core import Window, Sprite, Color

window = Window()

named_colors = [
    Color.AMBER,
    Color.AZURE,
    Color.BLUE,
    Color.CHARTREUSE,
    Color.CYAN,
    Color.GREEN,
    Color.MAGENTA,
    Color.ORANGE,
    Color.PURPLE,
    Color.RED,
    Color.ROSE,
    Color.TEAL,
    Color.VERMILION,
    Color.VIOLET,
    Color.YELLOW,
]

for i in range(len(named_colors)):
    s = window.create_sprite()
    s.scale_x = window.width
    s.scale_y = window.height/len(named_colors)
    s.color = named_colors[i]
    s.x = window.center.x
    s.y = (i + 0.5) * s.scale_y


class ColorSprite(Sprite):

    def on_create(self):
        self.goto_random_position()
        self.color = Color(0, 255, 100)
        self.opacity = randint(50, 150)
        self.scale_x = randint(50, 200)
        self.scale_y = randint(50, 200)


for _ in range(20):
    window.create_sprite(ColorSprite)


window.run()
