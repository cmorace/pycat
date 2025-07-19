#!/usr/bin/env python3
"""Test to verify that window offset functionality works correctly."""

import pytest
from pycat.core import Window
from pycat.geometry.point import Point


def test_offset_functionality():
    """Test that window offset functionality works correctly with modern matrix system."""
    # Create window
    window = Window(title="Test Window", width=400, height=300)
    
    # Test initial offset
    initial_offset = window.offset
    assert initial_offset is not None
    
    # Set a new offset
    new_offset = Point(50, 25)
    window.offset = new_offset
    
    # Test that the offset is properly stored
    assert window.offset.x == 50
    assert window.offset.y == 25
    
    # Create a sprite to test positioning
    sprite = window.create_sprite(x=100, y=100)
    
    # Verify sprite positioning works correctly
    assert sprite.x == 100
    assert sprite.y == 100
    
    # Test offset update functionality
    window.offset = Point(25, 12.5)
    assert window.offset.x == 25
    assert window.offset.y == 12.5
    
    # Clean up
    window.close()


def test_sprites_positioning():
    """Test that sprite positioning still works correctly."""
    window = Window(title="Test Window", width=400, height=300)
    
    # Create multiple sprites at different positions
    sprite1 = window.create_sprite(x=50, y=50)
    sprite2 = window.create_sprite(x=100, y=150)
    sprite3 = window.create_sprite(x=200, y=75)
    
    # Test positioning
    assert sprite1.x == 50 and sprite1.y == 50
    assert sprite2.x == 100 and sprite2.y == 150  
    assert sprite3.x == 200 and sprite3.y == 75
    
    # Test position changes
    sprite1.x = 75
    sprite1.y = 125
    
    assert sprite1.x == 75 and sprite1.y == 125
    
    # Test that sprites are managed properly in batch rendering
    all_sprites = window.get_all_sprites()
    assert len(all_sprites) == 3
    
    window.close()
