"""Test fixtures and utilities for pycat tests."""

import pytest
import os
from unittest.mock import Mock, patch
from typing import Generator

import pyglet
from pycat.core import Window
from pycat.sprite import Sprite
from pycat.label import Label


@pytest.fixture
def mock_window():
    """Create a mock window for testing without graphics."""
    with patch('pycat.base.base_window.PygletWindow') as mock_pyglet_window:
        mock_instance = Mock()
        mock_instance.get_size.return_value = (800, 600)
        mock_pyglet_window.return_value = mock_instance
        
        window = Window(width=800, height=600, title="Test Window")
        window._window = mock_instance
        yield window


@pytest.fixture
def headless_mode():
    """Set up headless mode for graphics tests."""
    # Set environment variable for headless mode
    os.environ['PYGLET_HEADLESS'] = '1'
    yield
    # Clean up
    if 'PYGLET_HEADLESS' in os.environ:
        del os.environ['PYGLET_HEADLESS']


@pytest.fixture
def test_image_path():
    """Path to a test image file."""
    # Create a simple test image if it doesn't exist
    test_dir = os.path.dirname(__file__)
    image_path = os.path.join(test_dir, 'test_image.png')
    
    if not os.path.exists(image_path):
        # Create a simple 32x32 red square image
        from PIL import Image as PILImage
        img = PILImage.new('RGB', (32, 32), color='red')
        img.save(image_path)
    
    yield image_path
    
    # Clean up if we created the file
    if os.path.exists(image_path):
        os.remove(image_path)


@pytest.fixture
def sample_sprite(mock_window):
    """Create a sample sprite for testing."""
    sprite = Sprite(mock_window)
    return sprite


@pytest.fixture
def sample_label():
    """Create a sample label for testing."""
    label = Label("Test Label", x=100, y=100)
    return label


class MockPygletWindow:
    """Mock pyglet window for testing."""
    
    def __init__(self, width=800, height=600, caption="Test"):
        self.width = width
        self.height = height
        self.caption = caption
        self._closed = False
    
    def get_size(self):
        return (self.width, self.height)
    
    def clear(self):
        pass
    
    def close(self):
        self._closed = True
    
    @property
    def closed(self):
        return self._closed


@pytest.fixture
def no_graphics():
    """Patch graphics-related functions for unit testing."""
    with patch.multiple(
        'pycat.window',
        glTexParameteri=Mock()
    ):
        yield


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as unit test (no graphics required)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (may require graphics)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "pyglet: mark test as pyglet compatibility test"
    )
    
    # Enable headless-like behavior for CI environments
    if os.environ.get('CI') or os.environ.get('PYCAT_HEADLESS'):
        # Mock graphics components early to avoid import issues
        import sys
        from unittest.mock import Mock
        
        # Mock pyglet modules that might cause issues in headless environments
        if 'pyglet.gl' not in sys.modules:
            sys.modules['pyglet.gl'] = Mock()
        if 'pyglet.graphics' not in sys.modules:
            sys.modules['pyglet.graphics'] = Mock()
