from pycat.base.event.key_event import KeyCode
from pycat.base.event.mouse_event import MouseEvent
from pycat.base.image import Image
from pycat.collision import is_buffered_rotated_box_collision
from pycat.sprite import Sprite
from pycat.window import Window

window = Window()


class RotatingSprite(Sprite):
    def on_create(self):
        self.set_image(Image.get_solid_color_texture(200, 100))
        self.position = window.center

    def on_update(self, dt):
        if window.get_key(KeyCode.SPACE):
            self.rotation += 1


s1 = window.create_sprite(RotatingSprite)


class DragSprite(Sprite):
    def on_create(self):
        self.set_image(Image.get_solid_color_texture(100, 200))
        self.position = window.center

    def on_mouse_drag(self, e: MouseEvent):
        p = e.position
        d = e.delta
        if self.contains_point(p) or self.contains_point(p-d):
            self.position += d

    def on_update(self, dt):
        if window.get_key(KeyCode.LEFT):
            self.rotation += 1
        if is_buffered_rotated_box_collision(self, s1, 20, 20):
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)


s2 = window.create_sprite(DragSprite)
window.add_window_event_listener(s2)
window.run()
