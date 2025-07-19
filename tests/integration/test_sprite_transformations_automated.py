#!/usr/bin/env python3
"""Automated tests for sprite transformations without requiring visual inspection."""

import pytest
from pycat.core import Window
from pycat.geometry.point import Point
from pyglet.math import Mat4, Vec3


class TestSpriteTransformations:
    """Test suite for sprite transformation functionality."""

    def test_sprite_positioning(self):
        """Test that sprites are positioned correctly."""
        window = Window(width=800, height=600)
        
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
        
        window.close()

    def test_sprite_rotation(self):
        """Test sprite rotation functionality."""
        window = Window(width=800, height=600)
        
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
        
        window.close()

    def test_sprite_scaling(self):
        """Test sprite scaling functionality."""
        window = Window(width=800, height=600)
        
        sprite = window.create_sprite(x=400, y=300)
        
        # Test initial scale
        assert sprite.scale == 1.0
        
        # Test scale changes
        sprite.scale = 2.0
        assert sprite.scale == 2.0
        
        sprite.scale = 0.5
        assert sprite.scale == 0.5
        
        # Test individual scale components if available
        if hasattr(sprite, 'scale_x') and hasattr(sprite, 'scale_y'):
            sprite.scale_x = 1.5
            sprite.scale_y = 0.8
            assert sprite.scale_x == 1.5
            assert sprite.scale_y == 0.8
        
        window.close()

    def test_window_offset_functionality(self):
        """Test that window offset is properly stored and applied."""
        window = Window(width=800, height=600)
        
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
        
        window.close()

    def test_matrix_transformations(self):
        """Test that matrix transformations work correctly."""
        window = Window(width=800, height=600)
        
        # Test that modern matrix classes are available
        translation_matrix = Mat4.from_translation(Vec3(10, 20, 0))
        assert translation_matrix is not None
        
        # Test matrix operations
        identity = Mat4()
        result = translation_matrix @ identity
        assert result is not None
        
        # Test that window can accept view matrix changes through internal pyglet window
        original_view = window._window.view
        window._window.view = translation_matrix
        # Note: We can't easily test the visual result, but we can test assignment works
        assert window._window.view is not None
        window._window.view = original_view  # Restore original
        
        window.close()

    def test_sprite_transformation_combinations(self):
        """Test combinations of sprite transformations."""
        window = Window(width=800, height=600)
        
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
        assert sprite.scale == 1.5
        
        # Test changing them in different orders
        sprite.scale = 2.0
        sprite.rotation = 90
        sprite.position = Point(400, 500)
        
        assert sprite.x == 400
        assert sprite.y == 500
        assert sprite.rotation == 90
        assert sprite.scale == 2.0
        
        window.close()

    def test_multiple_sprites_independence(self):
        """Test that multiple sprites maintain independent transformations."""
        window = Window(width=800, height=600)
        
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
        assert sprite1.scale == 0.8
        
        assert sprite2.rotation == 90
        assert sprite2.scale == 1.5
        
        assert sprite3.rotation == 180
        assert sprite3.scale == 2.0
        
        # Change one sprite and verify others are unaffected
        sprite2.x = 250
        sprite2.rotation = 135
        
        assert sprite1.rotation == 45  # Unchanged
        assert sprite3.rotation == 180  # Unchanged
        assert sprite2.rotation == 135  # Changed
        
        window.close()

    def test_window_offset_with_sprites(self):
        """Test window offset interaction with sprite positioning."""
        window = Window(width=800, height=600)
        
        sprite = window.create_sprite(x=400, y=300)
        
        # Store original sprite position
        original_x = sprite.x
        original_y = sprite.y
        
        # Apply window offset
        window.offset = Point(50, 25)
        
        # Sprite position should remain the same in its own coordinate system
        assert sprite.x == original_x
        assert sprite.y == original_y
        
        # Window offset should be applied during rendering (tested in drawing method)
        assert window.offset.x == 50
        assert window.offset.y == 25
        
        window.close()


def run_automated_transformation_tests():
    """Run all automated transformation tests."""
    print("Running automated sprite transformation tests...")
    
    test_suite = TestSpriteTransformations()
    
    tests = [
        ("Basic positioning", test_suite.test_sprite_positioning),
        ("Sprite rotation", test_suite.test_sprite_rotation),
        ("Sprite scaling", test_suite.test_sprite_scaling),
        ("Window offset", test_suite.test_window_offset_functionality),
        ("Matrix transformations", test_suite.test_matrix_transformations),
        ("Transformation combinations", test_suite.test_sprite_transformation_combinations),
        ("Multiple sprite independence", test_suite.test_multiple_sprites_independence),
        ("Window offset with sprites", test_suite.test_window_offset_with_sprites),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All automated transformation tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_automated_transformation_tests()
    if not success:
        exit(1)
