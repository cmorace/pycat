from pycat.geometry.point import Point


def line_intersection(
        ax: float,
        ay: float,
        bx: float,
        by: float,
        cx: float,
        cy: float,
        dx: float,
        dy: float,
        ) -> Point:
    d = ay*cx - by*cx - ax*cy + bx*cy - ay*dx + by*dx + ax*dy - bx*dy
    if abs(d) < 0.0001:
        # parallel lines
        # still need to check special case if lines overlap
        return None
    t1 = (bx*cy - bx*dy - by*cx + by*dx + cx*dy - cy*dx) / d
    t2 = (ay*bx - ax*by - ay*dx + by*dx + ax*dy - bx*dy) / d
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        # return t1 to test multiple intersections
        return Point(t1*ax + (1-t1)*bx, t1*ay + (1-t1)*by)
    return None

    # if sprite.is_moving_through(prev_position, other_sprite):
    #     sprite.get_intersecting_points(other_sprite)
