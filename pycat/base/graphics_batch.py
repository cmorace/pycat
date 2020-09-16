"""Implements the GraphicsBatch class"""
from pycat.base.sprite import Sprite
from pyglet.gl import GL_QUADS
from pyglet.graphics import Batch


class GraphicsBatch:
    def __init__(self):
        self._batch = Batch()

    def add_sprite(self, sprite: Sprite):
        sprite._sprite.batch = self._batch

    def remove_sprite(self, sprite: Sprite):
        """Removes a sprite from the batch.
        
        Deletes the vertex list from video memory.
        The sprite's texture is kept in video memory
        If it is safe to remove a sprite's texture from
        video memory you can use sprite._sprite.delete(), 
        which will also automatically remove it from the batch
        """
        null_batch = Batch()
        self._batch.migrate(vertex_list=sprite._sprite._vertex_list, 
                            mode=GL_QUADS,
                            group=sprite._sprite.group,
                            batch=null_batch)
        self._batch.invalidate()
        null_batch = Batch()

    def clear(self):
        self._batch = Batch()

    def draw(self):
        self._batch.draw()
