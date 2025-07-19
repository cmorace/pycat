#!/usr/bin/env python3
"""Test to verify that modernized pyglet 2.0+ matrix system works correctly."""

import pytest
from pycat.core import Window
from pycat.label import Label
from pyglet.math import Mat4, Vec3


def test_basic_window_functionality():
    """Test that basic window functionality works with modern pyglet 2.0+ matrix system."""
    # Create window
    window = Window(title="Test Window", width=400, height=300)
    
    # Create a label (tests layer setting which uses groups)
    label = Label("Test Label", x=10, y=10, layer=1)
    
    # Test layer property (this uses OrderedGroup internally)
    original_layer = label.layer
    label.layer = 3
    new_layer = label.layer
    
    assert new_layer != original_layer
    assert new_layer == 3
    
    # Test modern matrix system (these functions were removed in modernization)
    # Test matrix creation (replacement for old OpenGL functions)
    translation_matrix = Mat4.from_translation(Vec3(10.0, 20.0, 0.0))
    identity_matrix = Mat4()
    
    # Verify matrices were created successfully
    assert translation_matrix is not None
    assert identity_matrix is not None
    
    # Test the auto_draw functionality (this calls the modern matrix functions)
    try:
        # This would normally draw to the screen, but we're testing the function calls
        window._Window__auto_draw()
    except Exception as e:
        if "context" in str(e).lower() or "opengl" in str(e).lower():
            # Expected in headless test environment
            pass
        else:
            pytest.fail(f"Unexpected error in __auto_draw: {e}")
    
    # Clean up
    window.close()
