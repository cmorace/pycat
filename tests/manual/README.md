# Manual Tests

This directory contains tests that require visual inspection or manual interaction. These tests are not run automatically as part of the test suite.

## Running Manual Tests

### Visual Transformation Tests

Run the comprehensive visual test to verify sprite and window transformations work correctly:

```bash
cd tests/manual
python test_visual_transformations.py
```

This will open interactive windows to test:
- Basic sprite positioning
- Window offset functionality  
- Sprite rotations and scaling
- Animated transformations

### Legacy Visual Tests

For older visual tests:

```bash
python test_sprite_transformations_visual.py
```

## What to Look For

When running visual tests, verify:
- ✅ Sprites appear at correct labeled positions
- ✅ Grid moves smoothly with window offset changes
- ✅ Different rotations and scales display properly
- ✅ Smooth animations without glitches

If all visual elements work as expected, the sprite and window transformations are functioning correctly with the modern pyglet 2.0+ matrix system.
