from typing import Iterable, Tuple
from pyglet.shapes import Line
from pyglet.graphics import Batch

from pycat.collision import _get_sprite_basis_vectors, _get_sprite_vertices
from pycat.base.base_sprite import BaseSprite as Sprite


def draw_sprite_rects(sprites: Iterable[Sprite],
                      width: int = 3,
                      color: Tuple[int, int, int] = (255, 255, 255)):
    b = Batch()
    lines = []
    for sprite in sprites:
        axis = _get_sprite_basis_vectors(sprite)
        v = _get_sprite_vertices(sprite, axis)
        for i in range(-1, 3):
            line = Line(v[i].x, v[i].y, v[i+1].x, v[i+1].y, width, color, b)
            lines.append(line)
    b.draw()
