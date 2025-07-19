#!/usr/bin/env python3
"""Visual tests for sprite transformations to ensure they work correctly."""

from pycat.core import Window
from pycat.geometry.point import Point
from pycat.base.color import Color
import time


def test_basic_positioning():
    """Test basic sprite positioning at different locations."""
    print("Testing basic sprite positioning...")
    
    window = Window(title="Basic Positioning Test", width=800, height=600)
    
    # Create sprites at different positions
    sprites = []
    positions = [
        (100, 100, "Top-left area"),
        (400, 300, "Center"),
        (700, 500, "Bottom-right area"),
        (50, 300, "Left edge"),
        (750, 300, "Right edge"),
        (400, 50, "Top edge"),
        (400, 550, "Bottom edge")
    ]
    
    for i, (x, y, description) in enumerate(positions):
        sprite = window.create_sprite(x=x, y=y)
        # Use different colors to distinguish sprites
        colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, 
                 Color.CYAN, Color.MAGENTA, Color.WHITE]
        if hasattr(sprite, 'color'):
            sprite.color = colors[i % len(colors)]
        sprites.append((sprite, description))
    
    # Create labels to show what we're testing
    window.create_label(text="Basic Positioning Test", x=10, y=580, color=Color.WHITE)
    for i, (sprite, description) in enumerate(sprites):
        window.create_label(
            text=f"{description}: ({sprite.x}, {sprite.y})", 
            x=10, y=550 - i*20, 
            color=Color.WHITE
        )
    
    print("✓ Created sprites at various positions")
    print("  Visual check: Sprites should appear at labeled positions")
    return window


def test_window_offset():
    """Test window offset functionality."""
    print("\nTesting window offset...")
    
    window = Window(title="Window Offset Test", width=800, height=600)
    
    # Create a grid of sprites
    for x in range(100, 700, 100):
        for y in range(100, 500, 100):
            window.create_sprite(x=x, y=y)
    
    # Create reference labels
    window.create_label(text="Window Offset Test", x=10, y=580, color=Color.WHITE)
    window.create_label(text="Watch sprites move as offset changes", x=10, y=560, color=Color.WHITE)
    
    # Test different offsets
    offsets_to_test = [
        Point(0, 0),      # No offset
        Point(50, 25),    # Small offset
        Point(-30, 40),   # Negative X offset
        Point(0, -50),    # Negative Y offset
        Point(-25, -25),  # Both negative
    ]
    
    print("✓ Created grid of sprites")
    print("  Visual check: Grid should move as offset changes")
    
    return window, offsets_to_test


def test_sprite_properties():
    """Test various sprite properties and transformations."""
    print("\nTesting sprite properties...")
    
    window = Window(title="Sprite Properties Test", width=800, height=600)
    
    # Test different sprite properties
    test_cases = [
        {"x": 100, "y": 500, "rotation": 0, "scale": 1.0, "label": "Normal"},
        {"x": 200, "y": 500, "rotation": 45, "scale": 1.0, "label": "Rotated 45°"},
        {"x": 300, "y": 500, "rotation": 0, "scale": 1.5, "label": "Scaled 1.5x"},
        {"x": 400, "y": 500, "rotation": 90, "scale": 0.8, "label": "90° + 0.8x scale"},
        {"x": 500, "y": 500, "rotation": 180, "scale": 1.2, "label": "180° + 1.2x scale"},
        {"x": 600, "y": 500, "rotation": 270, "scale": 0.6, "label": "270° + 0.6x scale"},
    ]
    
    sprites = []
    for i, props in enumerate(test_cases):
        sprite = window.create_sprite(**{k: v for k, v in props.items() if k != "label"})
        sprites.append(sprite)
        
        # Create label for this test case
        window.create_label(
            text=props["label"], 
            x=props["x"] - 30, 
            y=props["y"] - 50, 
            color=Color.WHITE
        )
    
    window.create_label(text="Sprite Properties Test", x=10, y=580, color=Color.WHITE)
    window.create_label(text="Different rotations and scales", x=10, y=560, color=Color.WHITE)
    
    print("✓ Created sprites with different properties")
    print("  Visual check: Sprites should show different rotations and scales")
    
    return window, sprites


def test_dynamic_transformations():
    """Test dynamically changing sprite transformations."""
    print("\nTesting dynamic transformations...")
    
    window = Window(title="Dynamic Transformations Test", width=800, height=600)
    
    # Create sprites for animation
    center_sprite = window.create_sprite(x=400, y=300)
    moving_sprite = window.create_sprite(x=200, y=200)
    scaling_sprite = window.create_sprite(x=600, y=200) 
    rotating_sprite = window.create_sprite(x=200, y=400)
    combo_sprite = window.create_sprite(x=600, y=400)
    
    # Labels
    window.create_label(text="Dynamic Transformations Test", x=10, y=580, color=Color.WHITE)
    window.create_label(text="Center: Static", x=350, y=250, color=Color.WHITE)
    window.create_label(text="Moving", x=150, y=150, color=Color.WHITE)
    window.create_label(text="Scaling", x=550, y=150, color=Color.WHITE)
    window.create_label(text="Rotating", x=150, y=350, color=Color.WHITE)
    window.create_label(text="Combined", x=550, y=350, color=Color.WHITE)
    
    sprites_data = {
        'center': center_sprite,
        'moving': moving_sprite,
        'scaling': scaling_sprite,
        'rotating': rotating_sprite,
        'combo': combo_sprite
    }
    
    print("✓ Created sprites for dynamic testing")
    print("  Visual check: Sprites should animate with different transformations")
    
    return window, sprites_data


def run_visual_tests():
    """Run all visual tests."""
    print("=" * 60)
    print("SPRITE TRANSFORMATION VISUAL TESTS")
    print("=" * 60)
    print()
    print("These tests create visual windows to verify sprite transformations.")
    print("Close each window to proceed to the next test.")
    print("Press Ctrl+C to stop all tests.")
    print()
    
    try:
        # Test 1: Basic positioning
        window1 = test_basic_positioning()
        print("  → Window opened. Verify sprite positions match labels.")
        print("  → Close window to continue...")
        window1.run()
        
        # Test 2: Window offset
        window2, offsets = test_window_offset()
        print("  → Window opened. Testing different offsets...")
        
        # Animate through different offsets
        def update_offset(dt):
            current_time = time.time()
            offset_index = int(current_time * 0.5) % len(offsets)  # Change every 2 seconds
            window2.offset = offsets[offset_index]
        
        window2.run(update_function=lambda dt: update_offset(dt))
        
        # Test 3: Sprite properties
        window3, sprites = test_sprite_properties()
        print("  → Window opened. Verify different sprite transformations.")
        print("  → Close window to continue...")
        window3.run()
        
        # Test 4: Dynamic transformations
        window4, sprites_data = test_dynamic_transformations()
        print("  → Window opened. Sprites should animate continuously...")
        
        def animate_sprites(dt):
            current_time = time.time()
            
            # Moving sprite
            sprites_data['moving'].x = 200 + 100 * (1 + 0.8 * (current_time * 2) % 2 - 1)
            sprites_data['moving'].y = 200 + 50 * (1 + 0.6 * (current_time * 1.5) % 2 - 1)
            
            # Scaling sprite
            scale = 0.5 + 1.0 * abs((current_time * 1.0) % 2 - 1)
            sprites_data['scaling'].scale = scale
            
            # Rotating sprite
            sprites_data['rotating'].rotation = (current_time * 90) % 360
            
            # Combined transformations
            sprites_data['combo'].rotation = (current_time * 45) % 360
            combo_scale = 0.8 + 0.4 * abs((current_time * 0.8) % 2 - 1)
            sprites_data['combo'].scale = combo_scale
            sprites_data['combo'].x = 600 + 30 * (1 + (current_time * 3) % 2 - 1)
        
        window4.run(update_function=animate_sprites)
        
        print()
        print("=" * 60)
        print("✓ ALL VISUAL TESTS COMPLETED")
        print("=" * 60)
        print()
        print("If all sprites appeared and moved as expected, transformations are working correctly!")
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\n\nTest error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_visual_tests()
