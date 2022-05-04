from pycat.core import Window, Point, KeyCode
from pycat.math import dot

class FourWayMovementController:
    def __init__(self, window: Window, speed_factor: float = 10, friction_factor: float = 0.9):
        self._speed = Point()
        self._window = window
        self._speed_factor = speed_factor
        self._friction_factor = friction_factor

    @property
    def speed(self) -> float:
        return self._speed.magnitude()

    def get_direction_as_string(self) -> str:
        directions = {
            'up': dot(Point(0,1),self._speed),
            'down': dot(Point(0,-1),self._speed),
            'right': dot(Point(1,0),self._speed),
            'left': dot(Point(-1,0),self._speed),
        }
        max_direction_tuple = max(directions.items(), key=lambda x: x[1])
        return max_direction_tuple[0]

    def get_movement_delta(self, dt: float) -> Point:
        self._speed *= self._friction_factor

        player_input = Point()
        if self._window.is_key_pressed(KeyCode.W):
            player_input.y += 1            
        if self._window.is_key_pressed(KeyCode.S):
            player_input.y -= 1            
        if self._window.is_key_pressed(KeyCode.A):
            player_input.x -= 1            
        if self._window.is_key_pressed(KeyCode.D):
            player_input.x += 1        

        self._speed += player_input.normalized() * self._speed_factor
        
        return self._speed * dt 