"""The collision module defines functions to test for Sprite collision."""

from pycat.base.sprite import Sprite


def is_aabb_collision(a: Sprite, b: Sprite) -> bool:
    """Test for collision of two axis-aligned (non-rotated) sprites."""
    aw = a.width / 2
    bw = b.width / 2
    ah = a.height / 2
    bh = b.height / 2
    return (a.x - aw <= b.x + bw
        and a.x + aw >= b.x - bw
        and a.y - ah <= b.y + bh
        and a.y + ah >= b.y - bh)


def is_buffered_aabb_collision(a: Sprite, 
                               b: Sprite,
                               x_buffer: float = 0,
                               y_buffer: float = 0) -> bool:
    """Add buffer to axis-aligned collision detection."""
    aw = (a.width - x_buffer) / 2
    bw = (b.width - x_buffer) / 2
    ah = (a.height - y_buffer) / 2
    bh = (b.height - y_buffer) / 2
    return (a.x - aw <= b.x + bw
        and a.x + aw >= b.x - bw
        and a.y - ah <= b.y + bh
        and a.y + ah >= b.y - bh)


# for rotated bounding boxes
def is_rotated_box_collision(a: Sprite, b: Sprite):
    pass


def is_pixel_perfect_collision(a: Sprite, b: Sprite):
    pass
