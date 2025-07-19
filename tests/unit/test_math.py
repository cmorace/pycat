"""Unit tests for pycat math utilities."""

import pytest
import math
from pycat.math import (
    get_distance,
    get_degrees_from_direction,
    get_direction_from_degrees,
    get_rotated_point
)
from pycat.geometry.point import Point


class TestMathUtils:
    """Test cases for math utility functions."""

    @pytest.mark.unit
    def test_get_distance(self):
        """Test distance calculation between two points."""
        point1 = Point(0, 0)
        point2 = Point(3, 4)
        
        distance = get_distance(point1, point2)
        assert distance == 5.0
        
        # Test same point
        distance = get_distance(point1, point1)
        assert distance == 0.0
        
        # Test negative coordinates
        point3 = Point(-3, -4)
        distance = get_distance(point1, point3)
        assert distance == 5.0

    @pytest.mark.unit
    def test_get_degrees_from_direction(self):
        """Test conversion from direction vector to degrees."""
        # East (right)
        direction = Point(1, 0)
        degrees = get_degrees_from_direction(direction)
        assert abs(degrees - 0) < 0.01
        
        # North (up)
        direction = Point(0, 1)
        degrees = get_degrees_from_direction(direction)
        assert abs(degrees - 90) < 0.01
        
        # West (left)
        direction = Point(-1, 0)
        degrees = get_degrees_from_direction(direction)
        assert abs(degrees - 180) < 0.01 or abs(degrees + 180) < 0.01

    @pytest.mark.unit
    def test_get_direction_from_degrees(self):
        """Test conversion from degrees to direction vector."""
        # 0 degrees (East)
        direction = get_direction_from_degrees(0)
        assert abs(direction.x - 1.0) < 0.01
        assert abs(direction.y - 0.0) < 0.01
        
        # 90 degrees (North)
        direction = get_direction_from_degrees(90)
        assert abs(direction.x - 0.0) < 0.01
        assert abs(direction.y - 1.0) < 0.01
        
        # 180 degrees (West)
        direction = get_direction_from_degrees(180)
        assert abs(direction.x + 1.0) < 0.01
        assert abs(direction.y - 0.0) < 0.01

    @pytest.mark.unit
    def test_get_rotated_point(self):
        """Test point rotation around origin."""
        original_point = Point(1, 0)
        
        # Rotate 90 degrees
        rotated = get_rotated_point(original_point, 90)
        assert abs(rotated.x - 0.0) < 0.01
        assert abs(rotated.y - 1.0) < 0.01
        
        # Rotate 180 degrees
        rotated = get_rotated_point(original_point, 180)
        assert abs(rotated.x + 1.0) < 0.01
        assert abs(rotated.y - 0.0) < 0.01
        
        # Rotate 360 degrees (should be back to original)
        rotated = get_rotated_point(original_point, 360)
        assert abs(rotated.x - 1.0) < 0.01
        assert abs(rotated.y - 0.0) < 0.01

    @pytest.mark.unit
    def test_direction_degrees_roundtrip(self):
        """Test that converting degrees->direction->degrees gives original value."""
        original_degrees = 45.0
        direction = get_direction_from_degrees(original_degrees)
        converted_degrees = get_degrees_from_direction(direction)
        
        # Allow for small floating point errors
        assert abs(original_degrees - converted_degrees) < 0.01
