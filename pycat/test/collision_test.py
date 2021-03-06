from pycat.base.event.key_event import KeyCode
from pycat.base.event.mouse_event import MouseEvent
from pycat.base.image import Image
from pycat.collision import is_rotated_box_collision
from pycat.sprite import Sprite
from pycat.window import Window

window = Window()


class RotatingSprite(Sprite):
    def on_create(self):
        self.set_image(Image.get_solid_color_texture(200, 100))
        self.position = window.center

    def on_update(self, dt):
        if window.is_key_pressed(KeyCode.SPACE):
            self.rotation += 2


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
        if window.is_key_pressed(KeyCode.LEFT):
            self.rotation += 2
        elif window.is_key_pressed(KeyCode.RIGHT):
            self.rotation -= 2
        if is_rotated_box_collision(self, s1):
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)


s2 = window.create_sprite(DragSprite)
window.add_event_subscriber(s2)
window.run()
