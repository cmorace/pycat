from posixpath import dirname
from pycat.core import Window, Sprite
from pycat.experimental.level_entities import LevelData, get_levels_entities
from os.path import dirname
from typing import List

LEVEL_IMAGE_RELPATH = 'platformer/png/'
LDTK_PATH_PATH = dirname(__file__)+'/platformer.ldtk'
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

    def update_entities_x(self, dx):
        for s in self.sprites:
            s.x += dx

    def on_update(self, dt):
        if w.is_key_pressed('a'):
            prev_x = self.x
            self.x += self.speed
            self.x = min(self.x, self.width/2)
            self.update_entities_x(self.x-prev_x)
        if w.is_key_pressed('d'):
            prev_x = self.x
            self.x -= self.speed
            self.x = max(self.x, w.width-self.width/2)
            self.update_entities_x(self.x-prev_x)


level = w.create_sprite(ScrollableLevel)
levels_entities = get_levels_entities(LDTK_PATH_PATH)
level.create_entities(scale=3, level_entities=levels_entities[0])

w.run()
