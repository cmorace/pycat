from typing import List, Optional
from pycat.base.event.mouse_event import MouseEvent
from pycat.base.sound import Sound
from pycat.sprite import Sprite
from pycat.window import Window

window = Window()

sound_file = [
    "audio/die.wav", "audio/hit.wav", "audio/point.wav", "audio/swoosh.wav",
    "audio/wing.wav"
]

sound_fx: List[Sound] = []
for i in range(len(sound_file)):
    sound_fx.append(Sound(sound_file[i]))


class MusicalSprite1(Sprite):
    def on_create(self):
        self.image = "img/boom.png"
        self.scale = 0.2
        self.sound_fx: Optional[Sound] = None
        self.y = 0.33 * window.height

    def on_left_click(self):
        if self.sound_fx:
            self.sound_fx.play()


class MusicalSprite2(Sprite):
    def on_create(self):
        self.image = "img/eye.png"
        self.scale = 0.2
        self.sound_fx: Optional[Sound] = None
        self.y = .66 * window.height

    def on_mouse_press(self, e: MouseEvent):
        if self.sound_fx and self.contains_point(e.position):
            self.sound_fx.play()


dx = window.width / (len(sound_fx) + 1)
for i in range(len(sound_fx)):
    x = dx * (i + 1)

    s1 = window.create_sprite(MusicalSprite1)
    s1.x = x
    s1.sound_fx = sound_fx[i]

    s2 = window.create_sprite(MusicalSprite2)
    s2.x = x
    s2.sound_fx = sound_fx[i]
    window.add_event_subscriber(s2)

window.run()
