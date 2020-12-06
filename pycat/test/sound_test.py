from pycat.base.event import KeyCode, KeyEvent, MouseEvent
from pycat.sound import AudioLoop, Player, Sound
from pycat.core import Sprite, Window

window = Window(title="Sound Test")


class MusicalSprite1(Sprite):
    def setup(self, x: float, sound: Sound):
        self.position = (x, 0.33 * window.height)
        self.sound = sound
        self.image = "img/boom.png"
        self.scale = 0.2

    def on_left_click(self):
        self.sound.play()


class MusicalSprite2(Sprite):
    def setup(self, x: float, player: Player):
        self.position = (x, 0.66 * window.height)
        self.player = player
        self.image = "img/eye.png"
        self.scale = 0.5
        window.add_event_subscriber(self)

    def on_mouse_press(self, e: MouseEvent):
        if self.contains_point(e.position):
            self.player.play()


sound_file = [
    "audio/not_working/bonk.m4a",
    "audio/hit.wav",
    "audio/point.wav",
    "audio/swoosh.wav",
    "audio/wing.wav"
]

dx = window.width / (len(sound_file) + 1)
for i, file in enumerate(sound_file):
    x = dx * (i + 1)
    s1 = window.create_sprite(MusicalSprite1)
    s1.setup(x, Sound(file))
    s2 = window.create_sprite(MusicalSprite2)
    s2.setup(x, Player(file, volume=1, pitch=0.5))

background_player = AudioLoop("audio/LoopLivi.wav")
background_player.play()


def on_key_press(key: KeyEvent):
    if key == '1':
        background_player.set_audio("audio/LoopLivi.wav", play=True)
    elif key == '2':
        background_player.set_audio("audio/LoopSakamoto.wav", play=True)
    elif key == '3':
        background_player.set_audio("audio/not_working/Space Ambience.m4a",
                                    play=True)
    elif key == KeyCode.UP:
        background_player.volume += .1
    elif key == KeyCode.DOWN:
        background_player.volume -= .1
    elif key == KeyCode.RIGHT:
        background_player.pitch += .01
    elif key == KeyCode.LEFT:
        background_player.pitch -= .01
    elif key == KeyCode.SPACE:
        if background_player.is_playing:
            background_player.pause()
        else:
            background_player.play()


window.set_clear_color(175, 173, 213)
window.run(on_key_press=on_key_press)
