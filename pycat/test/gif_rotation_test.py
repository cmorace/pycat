from pycat.core import Window, Sprite, RotationMode, KeyCode

w = Window()


class TestGif(Sprite):

    def on_create(self):
        self.image = "img/bird_cropped.gif"
        self.rotation_mode = RotationMode.ALL_AROUND
        self.position = w.center

    def on_update(self, dt):
        if self.distance_to(w.mouse_position) > 10:
            self.point_toward_mouse_cursor()
            self.move_forward(10)

        if w.get_key_down(KeyCode._1):
            self.rotation_mode = RotationMode.ALL_AROUND
        elif w.get_key_down(KeyCode._2):
            self.rotation_mode = RotationMode.RIGHT_LEFT
        elif w.get_key_down(KeyCode._3):
            self.rotation_mode = RotationMode.MIRROR
        elif w.get_key_down(KeyCode._4):
            self.rotation_mode = RotationMode.NO_ROTATION


w.create_sprite(TestGif)
w.run()
