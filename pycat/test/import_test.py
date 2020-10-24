from pycat.core import Window, Sprite

w = Window()


class MyCustomSprite(Sprite):

    def on_create(self):
        self.add_tag("test")

    def on_update(self, dt):
        pass


w.run()
