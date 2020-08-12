from pycat.collision import is_buffered_aabb_collision
from pycat.sprite import Sprite

from pyglet.clock import schedule_interval as pyglet_schedule_interval
from pyglet.clock import unschedule as pyglet_unschedule

class SpriteList():

    @staticmethod
    def flatten_sprite_lists(sprite_lists):
        return [sprite for sprite_list in sprite_lists for sprite in sprite_list.__sprites]

    def __init__(self):
        self.__sprites = []

    def add(self, sprite):
        self.__sprites.append(sprite)
        sprite.on_create()
        pyglet_schedule_interval(sprite.on_update, 1/60)
        
    def remove(self, sprite: Sprite):
        self.__sprites.remove(sprite)
        pyglet_unschedule(sprite.on_update)

    def any_touching(self, other):
        for s in self.__sprites:
            if is_aabb_collision(s, other):
                return True
        return False

    def draw(self):
        for s in self.__sprites:
            s.draw()