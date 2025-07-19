# Testing pycat

This directory contains the pytest test suite for pycat.

## Test Structure

```
tests/
├── conftest.py              # Test fixtures and configuration
├── unit/                    # Unit tests (no graphics required)
│   ├── test_math.py        # Math utility tests
│   ├── test_point.py       # Point geometry tests
│   ├── test_color.py       # Color class tests
│   └── test_collision.py   # Collision detection tests
├── integration/             # Integration tests (may require graphics)
│   ├── test_window.py      # Window functionality tests
│   ├── test_sprite.py      # Sprite functionality tests
│   └── test_pyglet_compatibility.py  # Pyglet 2.0+ compatibility tests
└── fixtures/               # Test fixtures and sample data
```

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

Or install with test extras:
```bash
pip install -e .[test]
```

### Basic Test Commands

Run all tests:
```bash
pytest tests/
```

Run only unit tests (fast, no graphics required):
```bash
pytest tests/unit/ -m unit
```

Run only integration tests:
```bash
pytest tests/integration/ -m integration
```

Run pyglet compatibility tests:
```bash
pytest tests/ -m pyglet
```

### Using Makefile

The project includes a Makefile with convenient test commands:

```bash
make help           # Show available commands
make install-test   # Install test dependencies
make test          # Run all tests
make test-unit     # Run unit tests only
make test-integration  # Run integration tests only  
make test-pyglet   # Run pyglet compatibility tests
make test-coverage # Run tests with coverage report
make test-fast     # Run tests excluding slow ones
make test-headless # Run tests in headless mode
make clean         # Clean up test artifacts
```

### Headless Testing

For environments without a display (like CI), use headless mode:
```bash
make test-headless
```

Or set environment variable for custom headless testing:
```bash
PYCAT_HEADLESS=1 pytest tests/
```

The headless mode uses mocking to avoid graphics context issues on systems that don't support EGL or other graphics libraries.

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Fast tests that don't require graphics
- Test individual functions and classes in isolation
- Use mocks for external dependencies
- Should run in under a few seconds

### Integration Tests (`@pytest.mark.integration`)
- Test interaction between components
- May require graphics context (mocked in most cases)
- Test complete workflows and user scenarios

### Pyglet Compatibility Tests (`@pytest.mark.pyglet`)
- Specifically test pyglet 2.0+ compatibility
- Verify that compatibility layers work correctly
- Test that deprecated features have proper fallbacks

### Slow Tests (`@pytest.mark.slow`)
- Tests that take significant time to run
- Usually excluded from regular test runs
- Run with `pytest -m slow` when needed

## Writing Tests

### Test Naming
- Test files: `test_*.py`
- Test classes: `Test*`  
- Test functions: `test_*`

### Using Fixtures

Common fixtures are available in `conftest.py`:

```python
def test_something(mock_window, sample_sprite):
    # mock_window provides a mocked Window instance
    # sample_sprite provides a test Sprite
    assert sample_sprite.window == mock_window
```

### Mocking Graphics

For unit tests, use the provided fixtures to mock graphics:

```python
@pytest.mark.unit
def test_sprite_position(mock_window):
    sprite = Sprite(mock_window)
    sprite.position = Point(100, 200)
    assert sprite.position.x == 100
```

### Test Markers

Use appropriate markers for your tests:

```python
@pytest.mark.unit
def test_math_function():
    # Fast unit test
    pass

@pytest.mark.integration  
def test_window_sprite_interaction():
    # Integration test
    pass

@pytest.mark.slow
def test_performance_benchmark():
    # Slow test
    pass

@pytest.mark.pyglet
def test_pyglet_compatibility():
    # Pyglet compatibility test
    pass
```

## CI/CD

The project includes GitHub Actions workflows that:
- Run tests on multiple Python versions (3.8-3.11)
- Test on multiple operating systems (Linux, Windows, macOS)
- Generate coverage reports
- Run in headless mode for graphics tests

## Coverage

Generate coverage reports:
```bash
pytest tests/ --cov=pycat --cov-report=html --cov-report=term-missing
```

View HTML coverage report:
```bash
open htmlcov/index.html
```

## Troubleshooting

### Graphics Context Errors
If you see OpenGL or graphics context errors:

1. Use headless mode: `make test-headless`
2. Set environment variable: `PYCAT_HEADLESS=1 pytest tests/`
3. On Linux, you can also try xvfb: `xvfb-run -a pytest tests/`

### Import Errors
If you see import errors:
1. Install pycat in development mode: `pip install -e .`
2. Make sure all dependencies are installed: `pip install -r requirements-test.txt`

### Slow Tests
If tests are running slowly:
1. Run only unit tests: `pytest tests/unit/`
2. Skip slow tests: `pytest -m "not slow"`
3. Use parallel execution: `pip install pytest-xdist && pytest -n auto`
