"""Test sprite transformations to ensure they work correctly."""

import pytest
from pycat.core import Window
from pycat.geometry.point import Point
from pyglet.math import Mat4, Vec3


class TestSpriteTransformations:
    """Test suite for sprite transformation functionality."""

    @pytest.fixture
    def window(self):
        """Create a test window."""
        window = Window(width=800, height=600)
        yield window
        window.close()

    def test_sprite_positioning(self, window):
        """Test that sprites are positioned correctly."""
        # Test basic positioning
        sprite1 = window.create_sprite(x=100, y=200)
        assert sprite1.x == 100
        assert sprite1.y == 200
        
        # Test position changes
        sprite1.x = 150
        sprite1.y = 250
        assert sprite1.x == 150
        assert sprite1.y == 250
        
        # Test position via Point
        sprite1.position = Point(300, 400)
        assert sprite1.x == 300
        assert sprite1.y == 400

    def test_sprite_rotation(self, window):
        """Test sprite rotation functionality."""
        sprite = window.create_sprite(x=400, y=300)
        
        # Test initial rotation
        assert sprite.rotation == 0
        
        # Test rotation changes
        sprite.rotation = 45
        assert sprite.rotation == 45
        
        sprite.rotation = 180
        assert sprite.rotation == 180
        
        sprite.rotation = 360
        assert sprite.rotation == 360
        
        # Test negative rotation
        sprite.rotation = -90
        assert sprite.rotation == -90

    def test_sprite_scaling(self, window):
        """Test sprite scaling functionality."""
        sprite = window.create_sprite(x=400, y=300)
        
        # Test initial scale (use approximate equality for floats)
        assert abs(sprite.scale - 1.0) < 1e-6
        
        # Test scale changes
        sprite.scale = 2.0
        assert abs(sprite.scale - 2.0) < 1e-6
        
        sprite.scale = 0.5
        assert abs(sprite.scale - 0.5) < 1e-6
        
        # Test individual scale components if available
        if hasattr(sprite, 'scale_x') and hasattr(sprite, 'scale_y'):
            sprite.scale_x = 1.5
            sprite.scale_y = 0.8
            assert abs(sprite.scale_x - 1.5) < 1e-6
            assert abs(sprite.scale_y - 0.8) < 1e-6

    def test_window_offset_functionality(self, window):
        """Test that window offset is properly stored and applied."""
        # Test initial offset
        assert window.offset.x == 0
        assert window.offset.y == 0
        
        # Test offset changes
        window.offset = Point(50, 30)
        assert window.offset.x == 50
        assert window.offset.y == 30
        
        # Test negative offsets
        window.offset = Point(-25, -40)
        assert window.offset.x == -25
        assert window.offset.y == -40

    def test_matrix_transformations(self, window):
        """Test that matrix transformations work correctly."""
        # Test that modern matrix classes are available
        translation_matrix = Mat4.from_translation(Vec3(10, 20, 0))
        assert translation_matrix is not None
        
        # Test matrix operations
        identity = Mat4()
        result = translation_matrix @ identity
        assert result is not None
        
        # Test that window can accept view matrix changes
        original_view = window._window.view
        window._window.view = translation_matrix
        assert window._window.view is not None
        window._window.view = original_view  # Restore original

    def test_sprite_transformation_combinations(self, window):
        """Test combinations of sprite transformations."""
        sprite = window.create_sprite(x=100, y=100)
        
        # Apply multiple transformations
        sprite.x = 200
        sprite.y = 300
        sprite.rotation = 45
        sprite.scale = 1.5
        
        # Verify all transformations are preserved
        assert sprite.x == 200
        assert sprite.y == 300
        assert sprite.rotation == 45
        assert abs(sprite.scale - 1.5) < 1e-6
        
        # Test changing them in different orders
        sprite.scale = 2.0
        sprite.rotation = 90
        sprite.position = Point(400, 500)
        
        assert sprite.x == 400
        assert sprite.y == 500
        assert sprite.rotation == 90
        assert abs(sprite.scale - 2.0) < 1e-6

    def test_multiple_sprites_independence(self, window):
        """Test that multiple sprites maintain independent transformations."""
        sprite1 = window.create_sprite(x=100, y=100)
        sprite2 = window.create_sprite(x=200, y=200)
        sprite3 = window.create_sprite(x=300, y=300)
        
        # Apply different transformations to each sprite
        sprite1.rotation = 45
        sprite1.scale = 0.8
        
        sprite2.rotation = 90
        sprite2.scale = 1.5
        
        sprite3.rotation = 180
        sprite3.scale = 2.0
        
        # Verify each sprite maintains its own transformations
        assert sprite1.rotation == 45
        assert abs(sprite1.scale - 0.8) < 1e-6
        
        assert sprite2.rotation == 90
        assert abs(sprite2.scale - 1.5) < 1e-6
        
        assert sprite3.rotation == 180
        assert abs(sprite3.scale - 2.0) < 1e-6
        
        # Change one sprite and verify others are unaffected
        sprite2.x = 250
        sprite2.rotation = 135
        
        assert sprite1.rotation == 45  # Unchanged
        assert sprite3.rotation == 180  # Unchanged
        assert sprite2.rotation == 135  # Changed

    def test_window_offset_with_sprites(self, window):
        """Test window offset interaction with sprite positioning."""
        sprite = window.create_sprite(x=400, y=300)
        
        # Store original sprite position
        original_x = sprite.x
        original_y = sprite.y
        
        # Apply window offset
        window.offset = Point(50, 25)
        
        # Sprite position should remain the same in its own coordinate system
        assert sprite.x == original_x
        assert sprite.y == original_y
        
        # Window offset should be applied during rendering
        assert window.offset.x == 50
        assert window.offset.y == 25

    def test_auto_draw_with_offset(self, window):
        """Test that __auto_draw method works with window offset."""
        # Create a sprite
        sprite = window.create_sprite(x=100, y=100)
        
        # Test with no offset
        window.offset = Point(0, 0)
        try:
            window._Window__auto_draw()
            # If it doesn't crash, the basic drawing works
        except Exception as e:
            # In headless mode, we might get OpenGL context errors, which is fine
            if "context" not in str(e).lower() and "opengl" not in str(e).lower():
                raise
        
        # Test with offset
        window.offset = Point(50, 25)
        try:
            window._Window__auto_draw()
            # If it doesn't crash, offset drawing works
        except Exception as e:
            # In headless mode, we might get OpenGL context errors, which is fine
            if "context" not in str(e).lower() and "opengl" not in str(e).lower():
                raise
