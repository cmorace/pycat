from pycat.base.event.mouse_event import MouseEvent
from pycat.window import Window
from pycat.sprite import Sprite
from pycat.base.sound import Sound
from pycat.resource import set_resource_directory


window = Window()

sounds = ["audio/die.wav", 
          "audio/hit.wav",
          "audio/point.wav",
          "audio/swoosh.wav",
          "audio/wing.wav"]


class MusicalSprite1(Sprite):
    def on_create(self):
        self.image = "img/boom.png"
        self.scale = 0.2
        self.sound = None
        self.y = 0.33 * window.height

    def on_left_click(self):
        if self.sound:
            self.sound.play()


class MusicalSprite2(Sprite):
    def on_create(self):
        self.image = "img/eye.png"
        self.scale = 0.2
        self.sound = None
        self.y = .66 * window.height

    def on_mouse_release(self, e: MouseEvent):
        if self.sound and self.contains_point(e.position):
            self.sound.play()


dx = window.width/(len(sounds)+1)
for i in range(len(sounds)):
    x = dx * (i+1)
    s1 = window.create_sprite(MusicalSprite1)
    s1.x = x
    s1.sound = Sound(sounds[i])
    
    s2 = window.create_sprite(MusicalSprite2)
    s2.x = x
    s2.sound = Sound(sounds[i])
    window.add_window_event_listener(s2)

    

window.run()