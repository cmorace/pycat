def point_in_region(lower_left_corner, upper_right_corner, x, y):
    return (
            x >= lower_left_corner.x
        and x <= upper_right_corner.x
        and y >= lower_left_corner.y
        and y <= upper_right_corner.y)