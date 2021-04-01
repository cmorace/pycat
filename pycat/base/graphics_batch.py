"""Implements the GraphicsBatch class"""
from pycat.base.base_sprite import BaseSprite
from pycat.label import Label
from pyglet.gl import GL_QUADS
from pyglet.graphics import Batch as PygletBatch


class GraphicsBatch:
    def __init__(self):
        self._batch = PygletBatch()

    def add_sprite(self, sprite: BaseSprite):
        sprite._sprite.batch = self._batch

    def add_label(self, label: Label):
        label._label.batch = self._batch

    def remove_sprite(self, sprite: BaseSprite):
        """Removes a sprite from the batch.

        Deletes the vertex list from video memory.
        The sprite's texture is kept in video memory
        If it is safe to remove a sprite's texture from
        video memory you can use sprite._sprite.delete(),
        which will also automatically remove it from the batch
        """
        null_batch = PygletBatch()
        self._batch.migrate(vertex_list=sprite._sprite._vertex_list,
                            mode=GL_QUADS,
                            group=sprite._sprite.group,
                            batch=null_batch)

    def remove_label(self, label: Label):
        label._label.delete()

    def clear(self):
        self._batch = PygletBatch()

    def draw(self):
        self._batch.draw()
