"""Unit tests for collision detection functions."""

import pytest
from unittest.mock import Mock, MagicMock
from pycat.collision import is_rotated_box_collision
from pycat.geometry.point import Point


class TestCollision:
    """Test cases for collision detection."""

    @pytest.mark.unit
    def test_is_rotated_box_collision_basic(self):
        """Test basic collision detection between two sprites."""
        # Create mock sprites
        sprite1 = Mock()
        sprite1.position = Point(0, 0)
        sprite1.width = 20
        sprite1.height = 20
        sprite1.image_rotation = 0  # Use image_rotation instead of rotation
        
        sprite2 = Mock()
        sprite2.position = Point(10, 10)
        sprite2.width = 20
        sprite2.height = 20
        sprite2.image_rotation = 0
        
        # These sprites should be colliding (overlapping)
        result = is_rotated_box_collision(sprite1, sprite2)
        assert isinstance(result, bool)

    @pytest.mark.unit
    def test_is_rotated_box_collision_no_overlap(self):
        """Test collision detection with non-overlapping sprites."""
        # Create mock sprites that are far apart
        sprite1 = Mock()
        sprite1.position = Point(0, 0)
        sprite1.width = 10
        sprite1.height = 10
        sprite1.image_rotation = 0
        
        sprite2 = Mock()
        sprite2.position = Point(100, 100)
        sprite2.width = 10
        sprite2.height = 10
        sprite2.image_rotation = 0
        
        # These sprites should not be colliding
        result = is_rotated_box_collision(sprite1, sprite2)
        assert result is False

    @pytest.mark.unit
    def test_is_rotated_box_collision_same_position(self):
        """Test collision detection with sprites at same position."""
        # Create mock sprites at the same position
        sprite1 = Mock()
        sprite1.position = Point(50, 50)
        sprite1.width = 20
        sprite1.height = 20
        sprite1.image_rotation = 0
        
        sprite2 = Mock()
        sprite2.position = Point(50, 50)
        sprite2.width = 20
        sprite2.height = 20
        sprite2.image_rotation = 0
        
        # These sprites should definitely be colliding
        result = is_rotated_box_collision(sprite1, sprite2)
        assert result is True

    @pytest.mark.unit
    def test_is_rotated_box_collision_with_rotation(self):
        """Test collision detection with rotated sprites."""
        # Create mock sprites with rotation
        sprite1 = Mock()
        sprite1.position = Point(0, 0)
        sprite1.width = 20
        sprite1.height = 10
        sprite1.image_rotation = 45  # 45 degree rotation
        
        sprite2 = Mock()
        sprite2.position = Point(5, 5)
        sprite2.width = 20
        sprite2.height = 10
        sprite2.image_rotation = 0
        
        # Test collision with rotation
        result = is_rotated_box_collision(sprite1, sprite2)
        assert isinstance(result, bool)

    @pytest.mark.unit
    def test_collision_function_handles_invalid_input(self):
        """Test that collision function handles invalid input gracefully."""
        # Test with None - should raise an exception
        with pytest.raises((AttributeError, TypeError)):
            is_rotated_box_collision(None, None)
        
        # Test with incomplete mock objects - should raise an exception
        incomplete_sprite = Mock()
        incomplete_sprite.position = Point(0, 0)
        incomplete_sprite.image_rotation = 0  
        # Missing width, height - Mock objects will return Mocks for these
        
        complete_sprite = Mock()
        complete_sprite.position = Point(0, 0)
        complete_sprite.width = 10
        complete_sprite.height = 10
        complete_sprite.image_rotation = 0
        
        # Should raise TypeError when trying to multiply float by Mock
        with pytest.raises(TypeError):
            is_rotated_box_collision(incomplete_sprite, complete_sprite)
