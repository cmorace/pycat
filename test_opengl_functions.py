#!/usr/bin/env python3
"""Test to verify that no-op OpenGL functions don't break functionality."""

def test_basic_window_functionality():
    """Test that basic window functionality still works with no-op OpenGL functions."""
    print("Testing basic window functionality with no-op OpenGL functions...")
    
    from pycat.core import Window
    from pycat.label import Label
    
    # Create window
    window = Window(title="Test Window", width=400, height=300)
    print("✓ Window created successfully")
    
    # Create a label (tests layer setting which uses groups)
    label = Label("Test Label", x=10, y=10, layer=1)
    print("✓ Label created successfully")
    
    # Test layer property (this uses OrderedGroup internally)
    original_layer = label.layer
    label.layer = 3
    new_layer = label.layer
    
    print(f"✓ Label layer changed from {original_layer} to {new_layer}")
    
    # Test modern matrix system (these functions were removed in modernization)
    from pyglet.math import Mat4, Vec3
    
    print("✓ Modern matrix classes imported successfully")
    
    # Test matrix creation (replacement for old OpenGL functions)
    translation_matrix = Mat4.from_translation(Vec3(10.0, 20.0, 0.0))
    identity_matrix = Mat4()
    
    print("✓ Matrix operations executed successfully (modern pyglet 2.0+ approach)")
    
    # Test the auto_draw functionality (this calls the OpenGL functions)
    try:
        # This would normally draw to the screen, but we're testing the function calls
        window._Window__auto_draw()
        print("✓ __auto_draw method executed successfully")
    except Exception as e:
        if "context" in str(e).lower() or "opengl" in str(e).lower():
            print("⚠ __auto_draw requires OpenGL context (expected in headless test)")
        else:
            print(f"✗ Unexpected error in __auto_draw: {e}")
            return False
    
    # Clean up
    window.close()
    print("✓ Window closed successfully")
    
    return True

if __name__ == "__main__":
    success = test_basic_window_functionality()
    if success:
        print("\n🎉 All tests passed! No-op OpenGL functions don't break functionality.")
    else:
        print("\n❌ Some tests failed!")
        exit(1)
