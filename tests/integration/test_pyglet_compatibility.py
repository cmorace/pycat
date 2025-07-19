"""Tests for pyglet 2.0+ compatibility."""

import pytest
from unittest.mock import patch, Mock
import pyglet


class TestPygletCompatibility:
    """Test cases for pyglet 2.0+ compatibility."""

    @pytest.mark.pyglet
    def test_pyglet_version(self):
        """Test that we're using a compatible pyglet version."""
        version = pyglet.version
        major_version = int(version.split('.')[0])
        assert major_version >= 2, f"Expected pyglet 2.0+, got {version}"

    @pytest.mark.pyglet
    def test_core_imports(self):
        """Test that all core pycat imports work correctly."""
        # Test core imports work without errors
        from pycat.core import Window
        from pycat.sprite import Sprite
        from pycat.label import Label
        
        # Test that compatibility functions are available
        from pycat.base.base_sprite import _create_ordered_group
        from pycat.label import _create_ordered_group as label_create_ordered_group
        
        # These imports should not raise any exceptions
        assert Window is not None
        assert Sprite is not None
        assert Label is not None
        assert _create_ordered_group is not None
        assert label_create_ordered_group is not None

    @pytest.mark.pyglet
    def test_ordered_group_compatibility(self):
        """Test OrderedGroup compatibility layer."""
        # Test importing the compatibility layer
        from pycat.base.base_sprite import _create_ordered_group
        
        # Should create a group without raising an exception
        group = _create_ordered_group(1)
        assert group is not None
        
        # Should be a pyglet Group
        assert isinstance(group, pyglet.graphics.Group)

    @pytest.mark.pyglet
    def test_ordered_group_in_label(self):
        """Test OrderedGroup compatibility in Label class."""
        from pycat.label import _create_ordered_group
        
        # Should create a group without raising an exception
        group = _create_ordered_group(2)
        assert group is not None
        assert isinstance(group, pyglet.graphics.Group)

    @pytest.mark.pyglet
    def test_modern_matrix_usage(self):
        """Test that pyglet 2.0+ uses modern matrix approach instead of deprecated functions."""
        # Test importing modern matrix classes
        from pyglet.math import Mat4, Vec3
        
        # Should create matrices without raising an exception
        translation_matrix = Mat4.from_translation(Vec3(10, 20, 0))
        assert translation_matrix is not None
        assert isinstance(translation_matrix, Mat4)
        
        # Test that deprecated OpenGL functions are no longer used
        from pycat import window
        assert not hasattr(window, 'glPushMatrix')
        assert not hasattr(window, 'glPopMatrix') 
        assert not hasattr(window, 'glTranslatef')

    @pytest.mark.pyglet
    def test_graphics_group_order(self):
        """Test that Group class accepts order parameter."""
        from pyglet.graphics import Group
        
        # In pyglet 2.0+, Group should accept order parameter
        group = Group(order=5)
        assert group is not None

    @pytest.mark.pyglet
    @patch('pycat.base.base_sprite.OrderedGroup')  # Mock the actual import location
    def test_group_creation_fallback(self, mock_group_class):
        """Test group creation with both old and new API."""
        from pycat.base.base_sprite import _create_ordered_group
        
        # Test with pyglet 2.0+ API (order as keyword)
        mock_group_class.return_value = Mock()
        _create_ordered_group(3)
        
        # Should have called the mocked OrderedGroup
        assert mock_group_class.called

    @pytest.mark.pyglet
    def test_window_creation_compatibility(self):
        """Test that window creation works with pyglet 2.0+."""
        # This test requires actual pyglet functionality
        try:
            from pycat.core import Window
            # Create window with minimum size to reduce resource usage
            window = Window(width=100, height=100, title="Test")
            
            # Basic properties should work
            assert window.width > 0
            assert window.height > 0
            assert hasattr(window, 'run')
            assert hasattr(window, 'clear')
            
            # Clean up
            window.close()
        except Exception as e:
            # If window creation fails in headless environment, that's expected
            if "DISPLAY" in str(e) or "display" in str(e).lower():
                pytest.skip("Headless environment - cannot create window")
            else:
                raise

    @pytest.mark.pyglet
    def test_label_creation_compatibility(self):
        """Test that label creation works with pyglet 2.0+."""
        from pycat.label import Label
        
        # Should be able to create a label
        label = Label("Test Label", x=10, y=20, layer=1)
        assert label is not None
        
        # Should be able to change layer
        label.layer = 3
        assert label.layer == 3

    @pytest.mark.pyglet
    def test_sprite_group_assignment(self):
        """Test that sprites can be assigned to groups."""
        from unittest.mock import Mock
        from pycat.sprite import Sprite
        
        # Create a mock window
        mock_window = Mock()
        mock_window.width = 800
        mock_window.height = 600
        
        try:
            sprite = Sprite(mock_window)
            
            # Should be able to set layer (which uses groups internally)
            sprite.layer = 2
            assert sprite.layer == 2
            
        except Exception as e:
            # Some sprite functionality might require actual pyglet context
            if "context" in str(e).lower() or "gl" in str(e).lower():
                pytest.skip("Graphics context required for sprite creation")
            else:
                raise

    @pytest.mark.pyglet
    def test_basic_functionality_integration(self):
        """Integration test covering the basic functionality from the standalone test."""
        # Test window creation
        from pycat.core import Window
        window = Window(title="Test Window", width=400, height=300)
        
        # Verify window has expected methods
        assert hasattr(window, 'clear')
        assert hasattr(window, 'run')
        assert window.width == 400
        assert window.height == 300
        
        # Test label creation and layer setting
        from pycat.label import Label
        label = Label("Test Label", x=10, y=10, layer=1)
        
        # Test layer property (this uses OrderedGroup internally)
        label.layer = 3
        assert label.layer == 3
        
        # Clean up
        window.close()
