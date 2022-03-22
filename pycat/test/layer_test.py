from pycat.core import Window, Sprite


class ClickMe(Sprite):
    def on_left_click(self):
        self.layer = max([s.layer for s in sprites])+1


w = Window()
sprites = [
    w.create_sprite(ClickMe, image='img/dinosaur.png', x=600, y=400, layer=0),
    w.create_sprite(ClickMe, image='img/centaur.png', x=250, y=300, layer=2),
    w.create_sprite(ClickMe, image='img/scratch.png', x=450, y=300, layer=1),
    w.create_sprite(ClickMe, image='img/bear.png', x=150, y=300, layer=3),
]
w.run()
