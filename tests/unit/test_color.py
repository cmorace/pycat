"""Unit tests for Color class."""

import pytest
from pycat.base.color import Color


class TestColor:
    """Test cases for Color class."""

    @pytest.mark.unit
    def test_color_creation(self):
        """Test color creation with different parameters."""
        # Color requires RGB values
        c1 = Color(255, 255, 255)  # White
        assert c1.r == 255
        assert c1.g == 255
        assert c1.b == 255
        
        # Color with RGB values
        c2 = Color(255, 0, 128)
        assert c2.r == 255
        assert c2.g == 0
        assert c2.b == 128

    @pytest.mark.unit
    def test_color_boundaries(self):
        """Test color values are within valid ranges."""
        # Test with valid values
        c = Color(255, 0, 128)
        assert 0 <= c.r <= 255
        assert 0 <= c.g <= 255
        assert 0 <= c.b <= 255

    @pytest.mark.unit
    def test_color_equality(self):
        """Test color equality comparison."""
        c1 = Color(255, 128, 64)
        c2 = Color(255, 128, 64)
        c3 = Color(128, 255, 64)
        
        assert c1 == c2
        assert c1 != c3

    @pytest.mark.unit
    def test_predefined_colors(self):
        """Test predefined color constants if they exist."""
        # Check if common colors are defined
        color_names = ['WHITE', 'BLACK', 'RED', 'GREEN', 'BLUE', 'YELLOW', 'CYAN', 'MAGENTA']
        
        for color_name in color_names:
            if hasattr(Color, color_name):
                color = getattr(Color, color_name)
                # Color constants are RGB tuples, not Color instances
                assert hasattr(color, 'r')
                assert hasattr(color, 'g')
                assert hasattr(color, 'b')

    @pytest.mark.unit
    def test_color_string_representation(self):
        """Test string representation of color."""
        c = Color(255, 128, 64)
        str_repr = str(c)
        
        # Should contain RGB values
        assert "255" in str_repr
        assert "128" in str_repr
        assert "64" in str_repr

    @pytest.mark.unit
    def test_color_tuple_conversion(self):
        """Test conversion to tuple if available."""
        c = Color(255, 128, 64)
        
        # Check if tuple conversion method exists
        if hasattr(c, 'as_tuple') or hasattr(c, 'to_tuple'):
            if hasattr(c, 'as_tuple'):
                tuple_repr = c.as_tuple()
            else:
                tuple_repr = c.to_tuple()
            
            assert isinstance(tuple_repr, tuple)
            assert len(tuple_repr) >= 3
            assert tuple_repr[0] == 255
            assert tuple_repr[1] == 128
            assert tuple_repr[2] == 64
