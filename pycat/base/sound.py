from pyglet import options as driver_options
from pyglet import media
from pyglet.resource import media

driver_options['audio'] = ('openal', 'pulse', 'directsound', 'silent')

class Sound:
    def __init__(self, file: str):
        self.__sound = media(file, streaming=False)

    def play(self):
        self.__sound.play()

