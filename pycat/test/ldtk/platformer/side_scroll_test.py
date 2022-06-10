from os.path import dirname
from typing import List

from pycat.core import Sprite, Window
from pycat.experimental.ldtk_level_entities import (LevelData,
                                                    get_levels_entities)

LEVEL_IMAGE_RELPATH = 'platformer/png/'
LDTK_PATH = dirname(__file__)+'/platformer.ldtk'
w = Window(is_sharp_pixel_scaling=True,
           enforce_window_limits=False)


class ScrollableLevel(Sprite):
    def on_create(self):
        self.speed = 10
        self.sprites: List[Sprite] = []
        self.layer = -1

    def create_entities(self, scale: float, level_entities: LevelData):
        self.image = f'{LEVEL_IMAGE_RELPATH}{level_entities.id}.png'
        self.scale = scale
        self.x = level_entities.x + self.width/2
        self.y = level_entities.y + self.height/2
        for e in level_entities.entities:
            s = w.create_sprite(x=self.scale*e.x,
                                y=self.scale*e.y,
                                scale_x=self.scale*e.width,
                                scale_y=self.scale*e.height,
                                tags=e.tags,
                                opacity=110)
            self.sprites.append(s)

    def on_update(self, dt):
        if w.is_key_pressed('a'):
            w.offset.x += self.speed
            w.offset.x = min(w.offset.x, 0)
        if w.is_key_pressed('d'):
            w.offset.x -= self.speed
            w.offset.x = max(w.offset.x, w.width-self.width)


level = w.create_sprite(ScrollableLevel)
levels_entities = get_levels_entities(LDTK_PATH)
level.create_entities(scale=3, level_entities=levels_entities[0])

w.run()
