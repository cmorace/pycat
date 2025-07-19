"""Unit tests for Point geometry class."""

import pytest
from pycat.geometry.point import Point


class TestPoint:
    """Test cases for Point class."""

    @pytest.mark.unit
    def test_point_creation(self):
        """Test point creation with different parameters."""
        # Default point
        p1 = Point()
        assert p1.x == 0
        assert p1.y == 0
        
        # Point with coordinates
        p2 = Point(3, 4)
        assert p2.x == 3
        assert p2.y == 4
        
        # Point with negative coordinates
        p3 = Point(-2.5, -7.8)
        assert p3.x == -2.5
        assert p3.y == -7.8

    @pytest.mark.unit
    def test_point_addition(self):
        """Test point addition."""
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        
        result = p1 + p2
        assert result.x == 4
        assert result.y == 6
        
        # Addition with zero point
        zero = Point(0, 0)
        result = p1 + zero
        assert result.x == p1.x
        assert result.y == p1.y

    @pytest.mark.unit
    def test_point_subtraction(self):
        """Test point subtraction."""
        p1 = Point(5, 7)
        p2 = Point(2, 3)
        
        result = p1 - p2
        assert result.x == 3
        assert result.y == 4
        
        # Subtraction with itself
        result = p1 - p1
        assert result.x == 0
        assert result.y == 0

    @pytest.mark.unit
    def test_point_multiplication(self):
        """Test point multiplication by scalar."""
        p = Point(2, 3)
        
        # Multiply by positive scalar
        result = p * 2
        assert result.x == 4
        assert result.y == 6
        
        # Multiply by zero
        result = p * 0
        assert result.x == 0
        assert result.y == 0
        
        # Multiply by negative scalar
        result = p * -1
        assert result.x == -2
        assert result.y == -3

    @pytest.mark.unit
    def test_point_division(self):
        """Test point division by scalar."""
        p = Point(6, 8)
        
        # Divide by positive scalar
        result = p / 2
        assert result.x == 3
        assert result.y == 4
        
        # Divide by decimal
        result = Point(5, 10) / 2.5
        assert result.x == 2
        assert result.y == 4

    @pytest.mark.unit
    def test_point_division_by_zero(self):
        """Test that division by zero raises appropriate error."""
        p = Point(1, 2)
        
        with pytest.raises(ZeroDivisionError):
            p / 0

    @pytest.mark.unit
    def test_point_equality(self):
        """Test point equality comparison."""
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(2, 1)
        
        # Test that points with same coordinates have same x,y values
        assert p1.x == p2.x and p1.y == p2.y
        assert not (p1.x == p3.x and p1.y == p3.y)
        
        # If Point has __eq__ method, test it
        if hasattr(Point, '__eq__') and Point.__eq__ != object.__eq__:
            assert p1 == p2
            assert p1 != p3

    @pytest.mark.unit
    def test_point_str_representation(self):
        """Test string representation of point."""
        p = Point(1.5, -2.3)
        str_repr = str(p)
        
        assert "1.5" in str_repr
        assert "-2.3" in str_repr

    @pytest.mark.unit
    def test_point_magnitude(self):
        """Test point magnitude calculation if available."""
        p = Point(3, 4)
        
        # Check if magnitude method exists
        if hasattr(p, 'magnitude'):
            mag = p.magnitude()
            assert abs(mag - 5.0) < 0.01
        
        # Test zero point magnitude
        zero = Point(0, 0)
        if hasattr(zero, 'magnitude'):
            mag = zero.magnitude()
            assert mag == 0

    @pytest.mark.unit
    def test_point_normalization(self):
        """Test point normalization if available."""
        p = Point(3, 4)
        
        # Check if normalize method exists
        if hasattr(p, 'normalize'):
            normalized = p.normalize()
            # Normalized vector should have magnitude ~1
            if hasattr(normalized, 'magnitude'):
                mag = normalized.magnitude()
                assert abs(mag - 1.0) < 0.01
