"""The collision module defines functions to test for Sprite collision."""
from typing import Tuple

from pycat.base.sprite import Sprite
from pycat.geometry.point import Point
from pycat.math import dot, get_direction_from_degrees, project_p_onto_q


def is_aabb_collision(a: Sprite, b: Sprite) -> bool:
    """Test for collision of two axis-aligned (non-rotated) sprites."""
    aw = a.width / 2
    bw = b.width / 2
    ah = a.height / 2
    bh = b.height / 2
    return (a.x - aw <= b.x + bw and a.x + aw >= b.x - bw
            and a.y - ah <= b.y + bh and a.y + ah >= b.y - bh)


def is_buffered_aabb_collision(a: Sprite,
                               b: Sprite,
                               x_buffer: float = 0,
                               y_buffer: float = 0) -> bool:
    """Add buffer to axis-aligned collision detection."""
    aw = (a.width - x_buffer) / 2
    bw = (b.width - x_buffer) / 2
    ah = (a.height - y_buffer) / 2
    bh = (b.height - y_buffer) / 2
    return (a.x - aw <= b.x + bw and a.x + aw >= b.x - bw
            and a.y - ah <= b.y + bh and a.y + ah >= b.y - bh)


def _get_sprite_basis_vectors(a: Sprite) -> Tuple[Point, Point]:
    u = get_direction_from_degrees(a.rotation)
    v = Point(u.y, -u.x)
    return (u, v)


def _get_sprite_vertices(a: Sprite, basis: Tuple[Point, Point]) -> Tuple:
    u = basis[0] * a.width / 2
    v = basis[1] * a.height / 2
    p = a.position
    return (p + u + v, p - u + v, p - u - v, p + u - v)


def _get_projection_lengths(q, verts, origin):
    lengths = []
    for vertex in verts:
        p = vertex - origin
        projection = project_p_onto_q(p, q)
        lengths.append(dot(projection, q))
    return lengths


def is_rotated_box_collision(a: Sprite, b: Sprite):

    a_basis = _get_sprite_basis_vectors(a)
    a_vertices = _get_sprite_vertices(a, a_basis)
    b_basis = _get_sprite_basis_vectors(b)
    b_vertices = _get_sprite_vertices(b, b_basis)

    p = _get_projection_lengths(a_basis[0], b_vertices, a_vertices[2])
    if max(p) < 0 or min(p) > a.width:
        return False
    p = _get_projection_lengths(a_basis[1], b_vertices, a_vertices[2])
    if max(p) < 0 or min(p) > a.height:
        return False
    p = _get_projection_lengths(b_basis[0], a_vertices, b_vertices[2])
    if max(p) < 0 or min(p) > b.width:
        return False
    p = _get_projection_lengths(b_basis[1], a_vertices, b_vertices[2])
    if max(p) < 0 or min(p) > b.height:
        return False
    return True


def is_buffered_rotated_box_collision(a: Sprite, b: Sprite, x_buffer: float,
                                      y_buffer: float) -> bool:

    a_basis = _get_sprite_basis_vectors(a)
    a_vertices = _get_sprite_vertices(a, a_basis)
    b_basis = _get_sprite_basis_vectors(b)
    b_vertices = _get_sprite_vertices(b, b_basis)

    p = _get_projection_lengths(a_basis[0], b_vertices, a_vertices[2])
    if max(p) < x_buffer or min(p) > a.width - x_buffer:
        return False
    p = _get_projection_lengths(a_basis[1], b_vertices, a_vertices[2])
    if max(p) < y_buffer or min(p) > a.height - y_buffer:
        return False
    p = _get_projection_lengths(b_basis[0], a_vertices, b_vertices[2])
    if max(p) < x_buffer or min(p) > b.width - x_buffer:
        return False
    p = _get_projection_lengths(b_basis[1], a_vertices, b_vertices[2])
    if max(p) < y_buffer or min(p) > b.height - y_buffer:
        return False
    return True


def is_pixel_perfect_collision(a: Sprite, b: Sprite):
    pass
