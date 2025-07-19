"""Integration tests for Window class."""

import pytest
from unittest.mock import patch, Mock
from pycat.core import Window
from pycat.geometry.point import Point


class TestWindowIntegration:
    """Integration tests for Window functionality."""

    @pytest.mark.integration
    def test_window_creation_with_mock(self, mock_window):
        """Test window creation with mocked pyglet window."""
        window = mock_window
        
        # Test window properties
        assert window.width == 800
        assert window.height == 600
        assert isinstance(window.center, Point)
        assert window.center.x == 400
        assert window.center.y == 300

    @pytest.mark.integration
    def test_window_clear(self, mock_window):
        """Test window clear functionality."""
        window = mock_window
        
        # Should not raise an exception
        window.clear()

    @pytest.mark.integration
    def test_window_event_subscription(self, mock_window):
        """Test window event subscription."""
        window = mock_window
        
        def test_callback(event):
            pass
        
        # Should not raise an exception
        window.subscribe(on_key_press=test_callback)
        window.unsubscribe(on_key_press=test_callback)

    @pytest.mark.integration
    @patch('pyglet.app.run')
    def test_window_run(self, mock_app_run, mock_window):
        """Test window run method."""
        window = mock_window
        
        def test_draw():
            pass
        
        def test_update(dt):
            pass
        
        # Should call pyglet.app.run
        window.run(draw_function=test_draw, update_function=test_update)
        mock_app_run.assert_called_once()

    @pytest.mark.integration
    def test_window_close(self, mock_window):
        """Test window close functionality."""
        window = mock_window
        
        # Should not raise an exception
        window.close()
        window._window.close.assert_called_once()

    @pytest.mark.integration
    def test_window_screenshot(self, mock_window):
        """Test window screenshot functionality."""
        window = mock_window
        
        # Mock the buffer manager
        with patch('pycat.base.base_window.get_buffer_manager') as mock_get_buffer:
            mock_buffer = Mock()
            mock_color_buffer = Mock()
            mock_buffer.get_color_buffer.return_value = mock_color_buffer
            mock_get_buffer.return_value = mock_buffer
            
            # Should not raise an exception
            window.save_screen_shot("test.png")
            mock_color_buffer.save.assert_called_with("test.png")

    @pytest.mark.integration
    def test_window_set_clear_color(self, mock_window):
        """Test setting window clear color."""
        window = mock_window
        
        # Should not raise an exception
        window.set_clear_color(255, 0, 0, 255)  # Red color
