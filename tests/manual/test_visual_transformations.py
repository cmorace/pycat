#!/usr/bin/env python3
"""Visual test to verify sprite and window transformations work correctly."""

from pycat.core import Window
from pycat.geometry.point import Point
from pycat.base.color import Color
import time
import math


def test_basic_sprite_positioning():
    """Test basic sprite positioning at different locations."""
    print("=" * 60)
    print("BASIC SPRITE POSITIONING TEST")
    print("=" * 60)
    print("This test creates sprites at different positions.")
    print("You should see colored rectangles at labeled positions.")
    print("Close the window to continue to the next test.")
    print()
    
    window = Window(title="Basic Positioning Test", width=800, height=600, enforce_window_limits=False)
    
    # Create sprites at different positions with different colors
    positions_and_colors = [
        (100, 500, Color.RED, "Red - Top-left area"),
        (400, 300, Color.GREEN, "Green - Center"),
        (700, 100, Color.BLUE, "Blue - Bottom-right area"),
        (50, 300, Color.YELLOW, "Yellow - Left edge"),
        (750, 300, Color.CYAN, "Cyan - Right edge"),
        (400, 550, Color.MAGENTA, "Magenta - Top edge"),
        (400, 50, Color.WHITE, "White - Bottom edge")
    ]
    
    for x, y, color, description in positions_and_colors:
        sprite = window.create_sprite(x=x, y=y, scale=50.0)  # Make sprites 50x larger
        # Note: Color setting depends on sprite implementation
        window.create_label(text=description, x=x-50, y=y-30, color=color)
    
    # Instructions
    window.create_label(text="Basic Positioning Test", x=10, y=580, color=Color.WHITE)
    window.create_label(text="Sprites should appear at labeled positions", x=10, y=560, color=Color.WHITE)
    
    window.run()


def test_window_offset():
    """Test window offset functionality with animated offset changes."""
    print("=" * 60)
    print("WINDOW OFFSET TEST")
    print("=" * 60)
    print("This test shows a grid of sprites with changing window offset.")
    print("The entire grid should move smoothly as the offset changes.")
    print("Close the window to continue to the next test.")
    print()
    
    window = Window(title="Window Offset Test", width=800, height=600, enforce_window_limits=False)
    
    # Create a grid of sprites
    for x in range(100, 700, 100):
        for y in range(100, 500, 100):
            window.create_sprite(x=x, y=y, scale=50.0)  # Make grid sprites 50x larger
    
    # Instructions
    window.create_label(text="Window Offset Test - Grid Movement", x=10, y=580, color=Color.WHITE)
    window.create_label(text="Watch the grid move as offset changes", x=10, y=560, color=Color.WHITE)
    
    start_time = time.time()
    
    def update_with_offset(dt):
        current_time = time.time() - start_time
        
        # Create smooth circular motion for the offset
        radius = 50
        offset_x = radius * math.cos(current_time)
        offset_y = radius * math.sin(current_time * 1.5)
        
        window.offset = Point(offset_x, offset_y)
    
    window.run(update_function=update_with_offset)


def test_sprite_transformations():
    """Test various sprite transformations."""
    print("=" * 60)
    print("SPRITE TRANSFORMATIONS TEST")
    print("=" * 60)
    print("This test shows sprites with different rotations and scales.")
    print("You should see sprites with various transformations applied.")
    print("Close the window to continue to the next test.")
    print()
    
    window = Window(title="Sprite Transformations Test", width=800, height=600, enforce_window_limits=False)
    
    # Create sprites with different transformations
    transformations = [
        {"x": 100, "y": 400, "rotation": 0, "scale": 50.0, "label": "Normal (0°, 50.0x)"},
        {"x": 250, "y": 400, "rotation": 45, "scale": 50.0, "label": "45° rotation"},
        {"x": 400, "y": 400, "rotation": 0, "scale": 60.0, "label": "60.0x scale"},
        {"x": 550, "y": 400, "rotation": 90, "scale": 40.0, "label": "90°, 40.0x scale"},
        {"x": 700, "y": 400, "rotation": 180, "scale": 55.0, "label": "180°, 55.0x scale"},
    ]
    
    for props in transformations:
        sprite = window.create_sprite(
            x=props["x"], 
            y=props["y"], 
            rotation=props["rotation"], 
            scale=props["scale"]
        )
        
        # Create label for this transformation
        window.create_label(
            text=props["label"], 
            x=props["x"] - 60, 
            y=props["y"] - 80, 
            color=Color.WHITE
        )
    
    # Instructions
    window.create_label(text="Sprite Transformations Test", x=10, y=580, color=Color.WHITE)
    window.create_label(text="Different rotations and scales applied to sprites", x=10, y=560, color=Color.WHITE)
    
    window.run()


def test_animated_transformations():
    """Test dynamically changing sprite transformations."""
    print("=" * 60)
    print("ANIMATED TRANSFORMATIONS TEST")
    print("=" * 60)
    print("This test shows sprites with continuously changing transformations.")
    print("You should see sprites rotating, scaling, and moving smoothly.")
    print("Close the window to finish all tests.")
    print()
    
    window = Window(title="Animated Transformations Test", width=800, height=600, enforce_window_limits=False)
    
    # Create sprites for different types of animation
    center_sprite = window.create_sprite(x=400, y=300, scale=50.0)  # Static reference, much larger
    rotating_sprite = window.create_sprite(x=200, y=200, scale=50.0)
    scaling_sprite = window.create_sprite(x=600, y=200, scale=50.0)
    moving_sprite = window.create_sprite(x=200, y=400, scale=50.0)
    combo_sprite = window.create_sprite(x=600, y=400, scale=50.0)
    
    # Labels
    window.create_label(text="Animated Transformations Test", x=10, y=580, color=Color.WHITE)
    window.create_label(text="Center (static)", x=350, y=250, color=Color.WHITE)
    window.create_label(text="Rotating", x=150, y=150, color=Color.WHITE)
    window.create_label(text="Scaling", x=550, y=150, color=Color.WHITE)
    window.create_label(text="Moving", x=150, y=350, color=Color.WHITE)
    window.create_label(text="Combined", x=550, y=350, color=Color.WHITE)
    
    start_time = time.time()
    
    def animate_sprites(dt):
        current_time = time.time() - start_time
        
        # Rotating sprite - continuous rotation
        rotating_sprite.rotation = (current_time * 60) % 360  # 60 degrees per second
        
        # Scaling sprite - pulsing scale
        scale = 40.0 + 20.0 * math.sin(current_time * 2)  # Scale between 20.0 and 60.0
        scaling_sprite.scale = max(10.0, scale)  # Prevent scale from going too small
        
        # Moving sprite - figure-8 motion
        moving_sprite.x = 200 + 50 * math.sin(current_time)
        moving_sprite.y = 400 + 30 * math.sin(current_time * 2)
        
        # Combined sprite - rotation + scaling + small movement
        combo_sprite.rotation = (current_time * 90) % 360
        combo_scale = 35.0 + 15.0 * math.sin(current_time * 1.5)  # Scale between 20.0 and 50.0
        combo_sprite.scale = max(15.0, combo_scale)  # Prevent scale from going too small
        combo_sprite.x = 600 + 20 * math.cos(current_time * 0.5)
        combo_sprite.y = 400 + 15 * math.sin(current_time * 0.7)
    
    window.run(update_function=animate_sprites)


def main():
    """Run all visual tests."""
    print("PYCAT SPRITE AND WINDOW TRANSFORMATION VISUAL TESTS")
    print("=" * 60)
    print()
    print("These tests will open windows to visually verify that:")
    print("1. Sprites appear at correct positions")
    print("2. Window offset moves all content together")
    print("3. Sprite rotations and scales work correctly")
    print("4. Animated transformations update smoothly")
    print()
    print("Close each window to proceed to the next test.")
    print("Press Ctrl+C to exit early if needed.")
    print()
    input("Press Enter to start the tests...")
    print()
    
    try:
        # Run each test
        test_basic_sprite_positioning()
        test_window_offset()
        test_sprite_transformations()
        test_animated_transformations()
        
        print()
        print("=" * 60)
        print("✅ ALL VISUAL TESTS COMPLETED!")
        print("=" * 60)
        print()
        print("If you saw:")
        print("• Sprites at correct labeled positions")
        print("• Grid moving smoothly with offset changes")
        print("• Different rotations and scales on sprites")
        print("• Smooth animations without glitches")
        print()
        print("Then sprite and window transformations are working correctly! 🎉")
        
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
