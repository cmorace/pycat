from .sprite import Sprite
from .geometry.point import Point
from .math import get_square_distance
# this module will perform different type of collision testing
# 1. two points are within some distance

# todo:
# 3. two arbitrary oriented rectangles are intersecting
# 4. two convex polygons are intersecting

# axis aligned bounding box collision
def is_aabb_collision(a: Sprite, b: Sprite) -> bool:
    aw = a.width/2
    bw = b.width/2
    ah = a.height/2
    bh = b.height/2
    return (a.x - aw <= b.x + bw and a.x + aw >= b.x - bw and
           a.y - ah <= b.y + bh and a.y + ah >= b.y - bh)

# axis aligned bounding box collision
def is_buffered_aabb_collision(a: Sprite, b: Sprite, x_buffer:float=0, y_buffer:float=0) -> bool:
    aw = (a.width-x_buffer)/2 
    bw = (b.width-x_buffer)/2
    ah = (a.height-y_buffer)/2
    bh = (b.height-y_buffer)/2
    return (a.x - aw <= b.x + bw and a.x + aw >= b.x - bw and
           a.y - ah <= b.y + bh and a.y + ah >= b.y - bh)


# for rotated bounding boxes
def is_bounding_box_collision(a: Sprite, b: Sprite):
    pass

def is_pixel_perfect_collision(a: Sprite, b: Sprite):
    pass