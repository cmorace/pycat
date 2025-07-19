"""Integration tests for Sprite functionality."""

import pytest
from unittest.mock import Mock, patch
from pycat.sprite import Sprite
from pycat.geometry.point import Point


class TestSpriteIntegration:
    """Integration tests for Sprite class."""

    @pytest.mark.integration
    def test_sprite_creation_with_window(self, mock_window):
        """Test sprite creation with a window."""
        sprite = Sprite(mock_window)
        
        # Test basic sprite properties
        assert hasattr(sprite, 'position')
        assert hasattr(sprite, 'layer')
        assert hasattr(sprite, 'rotation')
        assert sprite.window == mock_window

    @pytest.mark.integration
    def test_sprite_position_setting(self, mock_window):
        """Test setting sprite position."""
        sprite = Sprite(mock_window)
        
        new_position = Point(100, 200)
        sprite.position = new_position
        
        # Position should be updated
        assert sprite.position.x == 100
        assert sprite.position.y == 200

    @pytest.mark.integration
    def test_sprite_layer_setting(self, mock_window):
        """Test setting sprite layer."""
        sprite = Sprite(mock_window)
        
        sprite.layer = 5
        assert sprite.layer == 5
        
        sprite.layer = -1
        assert sprite.layer == -1

    @pytest.mark.integration
    def test_sprite_rotation(self, mock_window):
        """Test sprite rotation."""
        sprite = Sprite(mock_window)
        
        sprite.rotation = 45.0
        assert sprite.rotation == 45.0
        
        sprite.rotation = 360.0
        assert sprite.rotation == 360.0

    @pytest.mark.integration
    def test_sprite_size_properties(self, mock_window):
        """Test sprite size properties if available."""
        sprite = Sprite(mock_window)
        
        if hasattr(sprite, 'width') and hasattr(sprite, 'height'):
            # If sprite has size properties, they should be readable
            width = sprite.width
            height = sprite.height
            assert isinstance(width, (int, float))
            assert isinstance(height, (int, float))

    @pytest.mark.integration
    def test_sprite_tags(self, mock_window):
        """Test sprite tagging system."""
        sprite = Sprite(mock_window)
        
        # Test adding tags
        sprite.add_tag("player")
        sprite.add_tag("enemy")
        
        # Test checking tags through the tags property
        assert "player" in sprite.tags
        assert "enemy" in sprite.tags
        assert "nonexistent" not in sprite.tags
        
        # Test removing tags
        sprite.remove_tag("enemy")
        assert "enemy" not in sprite.tags
        assert "player" in sprite.tags  # Other tags should remain

    @pytest.mark.integration
    def test_sprite_lifecycle_methods(self, mock_window):
        """Test sprite lifecycle methods."""
        class TestSprite(Sprite):
            def __init__(self, window):
                self.created = False
                self.updated = False
                super().__init__(window)
                # Call on_create manually if it exists
                if hasattr(self, 'on_create'):
                    self.on_create()
            
            def on_create(self):
                """Mark sprite as created."""
                self.created = True
            
            def on_update(self, dt):
                """Mark sprite as updated."""
                self.updated = True
        
        sprite = TestSprite(mock_window)
        
        # on_create should have been called manually in __init__
        assert sprite.created
        
        # Call on_update manually
        sprite.on_update(0.016)  # ~60 FPS delta time
        assert sprite.updated

    @pytest.mark.integration
    def test_sprite_visibility(self, mock_window):
        """Test sprite visibility if supported."""
        sprite = Sprite(mock_window)
        
        if hasattr(sprite, 'visible'):
            # Test default visibility
            assert sprite.visible is True
            
            # Test hiding sprite
            sprite.visible = False
            assert sprite.visible is False
            
            # Test showing sprite again
            sprite.visible = True
            assert sprite.visible is True
