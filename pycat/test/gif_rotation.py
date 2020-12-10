from pycat.core import Window, Sprite, RotationMode, KeyCode

w = Window()


class TestGif(Sprite):

    def on_create(self):
        self.image = "img/tornado.gif"
        self.rotation_mode = RotationMode.ALL_AROUND
        self.position = w.center

    def on_update(self, dt):
        self.point_toward_mouse_cursor()
        self.move_forward(5)

        if w.get_key_down(KeyCode._1):
            self.rotation_mode = RotationMode.ALL_AROUND
        elif w.get_key_down(KeyCode._2):
            self.rotation_mode = RotationMode.RIGHT_LEFT
        elif w.get_key_down(KeyCode._3):
            self.rotation_mode = RotationMode.MIRROR


w.create_sprite(TestGif)
w.run()
