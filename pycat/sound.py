"""The sound module implements the Sound, Player, and AudioLoop classes.

Only .wav files are supported unless ffmpeg is installed (tested on MacOs).
A file converter can be found here -(https://online-audio-converter.com/)
"""
from pyglet import options as driver_options
from pyglet.resource import media
from pyglet.media import Player as PygletPlayer
from pyglet.media import Source, SourceGroup

driver_options['audio'] = ('openal', 'pulse', 'directsound', 'silent')


class Player:
    def __init__(self, file: str, volume: float = 0.5, pitch: float = 1):
        self._sound: Source = media(file, streaming=False)  # type: ignore
        self._player = PygletPlayer()
        self._player.queue(self._sound)
        self.volume = volume
        self.pitch = pitch
        self._player.on_player_eos = self.__on_empty_queue

    @property
    def is_playing(self):
        return self._player.playing

    def play(self):
        """Start playing the sound."""
        self.__reset(self._player.volume, self._player.pitch)  # type: ignore
        self._player.play()

    def pause(self):
        self._player.pause()

    @property
    def pitch(self) -> float:
        """The pitch shift to apply to the sound.

        The nominal pitch is 1.0. A pitch of 2.0 will sound one octave higher,
        and play twice as fast. A pitch of 0.5 will sound one octave lower, and
        play twice as slow. A pitch of 0.0 is not permitted.
        """
        return self._player.pitch  # type: ignore

    @pitch.setter
    def pitch(self, pitch: float):
        self._player.pitch = pitch

    @property
    def volume(self):
        """Volume of the played sound.

        volume ranges from 0 to 1
        """
        return self._player.volume

    @volume.setter
    def volume(self, vol: float):
        self._player.volume = vol

    def __on_empty_queue(self):
        self._player.queue(self._sound)
        pass

    def __reset(self, volume: float, pitch: float):
        # restart the sound if the player is already playing
        self._player.delete()
        self._player = PygletPlayer()
        self._player.queue(self._sound)
        self.volume = volume
        self.pitch = pitch


class AudioLoop:
    def __init__(self, file: str, volume: float = 0.5, pitch: float = 1):
        # self._sound: Source = media(file, streaming=False)  # type: ignore
        # self._source_group = SourceGroup()
        # self._player = PygletPlayer()
        # dummy is used to add new sound to source group when loop is complete
        # self.__dummy = PygletPlayer()
        # self.reset(volume, pitch)
        self.set_audio(file, volume, pitch)

    def set_audio(self, file: str, volume: float = 0.5, pitch: float = 1,
                  play: bool = False):
        self._sound: Source = media(file, streaming=False)  # type: ignore
        self._source_group = SourceGroup()
        self._player = PygletPlayer()
        # dummy is used to add new sound to source group when loop is complete
        self.__dummy = PygletPlayer()
        self.reset(volume, pitch)
        if play:
            self.play()

    def play(self):
        self.__dummy.play()
        self._player.play()

    def pause(self):
        self._player.pause()
        self.__dummy.pause()

    def reset(self, volume: float = 0.5, pitch: float = 1):
        # gapless playback only possible with SourceGroup
        self._source_group = SourceGroup()
        self._source_group.add(self._sound)
        self._source_group.add(self._sound)
        self._player = PygletPlayer()
        self._player.queue(self._source_group)
        self._player.on_player_eos = self.__restart
        self.volume = volume
        self.pitch = pitch
        # when the dummy's queue is empty, we add a new loop source to player
        self.__dummy = PygletPlayer()
        self.__dummy.queue(self._sound)
        self.__dummy.volume = 0
        self.__dummy.on_player_eos = self.__add_loop_source

    def __restart(self):
        self.reset(self._player.volume, self._player.pitch)  # type: ignore
        self.play()

    @property
    def is_playing(self) -> bool:
        return self._player.playing

    @property
    def pitch(self):
        return self._player.pitch

    @pitch.setter
    def pitch(self, pitch: float):
        self.__dummy.pitch = pitch
        self._player.pitch = pitch

    @property
    def volume(self):
        return self._player.volume

    @volume.setter
    def volume(self, volume: float):
        self._player.volume = volume

    def __add_loop_source(self):
        self.__dummy.queue(self._sound)
        self.__dummy.play()
        self._source_group.add(self._sound)
