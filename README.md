# pycat: A Python game framework simplifying game developement with pyglet.

## Students: To install or update 

run `pip install git+https://bitbucket.org/dwhite0/pycat.git -U`

## To install for development

run ```pip install -e .``` from the directory holding ```setup.py```



# User Guide

## Imports

```python
from pycat.core import Window, Sprite, Label, Color, Point, KeyCode, Scheduler, RotationMode

from pycat.base import MouseEvent, MouseButton, NumpyImage

from pycat.experimental.ldtk import LdtkFile
from pycat.experimental.spritesheet import SpriteSheet, UniversalLPCSpritesheet
from pycat.experimental.movement import FourWayMovementController
from pycat.experimental.animation import Animator
```

## Window

### Creating a Window

```python
window = Window()

# Place your code here

window.run()
```

`window.run()` should be the final line in the file.

### Managing sprites

```python
window.get_all_sprites()
window.get_sprites_with_tag('enemy')

window.delete_all_sprites()
window.delete_sprites_with_tag('enemy')
```

## Sprites

### Creating Sprites & Setting Their Initial Properties

#### Method 1

Name each property when creating the sprite as `property_name=value`. This method is suitable when the sprite is simple and not repeated elsewhere in your program.

```python
window.create_sprite(scale=100, x=200)
```

#### Method 2

Create a `class` to represent the sprite. Set properties inside the class using `self.property_name=value`.

```python
class Player(Sprite):
    def on_create(self):
        self.scale = 100
        self.x = 200

window.create_sprite(Player)
```

#### Method 3

Save the value from `create_sprite` in a variable to modify its properties after creation.

```python
player = window.create_sprite(scale=100)
player.x = 200
```

#### Combinations

All three methods may be combined. However, note the ordering carefully: 

1. properties are set in `on_create`, so `x=200` at the beginning
2. `create_sprite` may override properties, so `x=200` is changed to `x=300`
3. properties may be modified after creation, so finally `x=300` is changed to `x=400`

```python
class Player(Sprite):
    def on_create(self):
        self.scale = 100
        self.x = 200

player = window.create_sprite(Player, x=300)
player.x = 400
```

### Updating a sprite

The section above described how to do things **one time** when a sprite is created. To modify a sprite **lots of times** during the game we use `on_update()`. This method is called in every frame, which is about 60 times per second.

```python
class Player(Sprite):
    def on_update(self,dt):
        self.x += 10
```

### Sprite properties

#### Position

#### Rotation

Normally a sprite will rotate based on its `self.rotation` property. However, if you want to override that you can set `self.rotation_mode`:

```python
def on_create(self):
    self.rotation_mode = RotationMode.ALL_AROUND
    self.rotation_mode = RotationMode.RIGHT_LEFT
    self.rotation_mode = RotationMode.MIRROR
    self.rotation_mode = RotationMode.NO_ROTATION
```

#### Appearance

#### Tags

### Sprite collisions

Sprite collisions are usually checked in `on_update`.

Check if sprites are touching. These methods return a `bool` and are usually used in with `if`:

```python
def on_update(self,dt):
    if self.is_touching_any_sprite():
        self.delete()

    if self.is_touching_any_sprite_with_tag('enemy'):
        self.delete()

    if self.is_touching_sprite(player):
        self.delete()
```

Get the sprites that are touching. These methods return a list of `Sprite` and are usually used in a `for` loop:

```python
def on_update(self,dt):
    for sprite in self.get_touching_sprites():
        sprite.delete()

    for sprite in self.get_touching_sprites_with_tag('enemy'):
        sprite.delete()
```

## Label

### Creating Labels & Setting Their Initial Properties

A label can be created with inital properties in the same way as a sprite.

#### Method 1

```python
window.create_label(text='Score: 10')
```

#### Method 2

```python
class ScoreLabel(Label):
    def on_create(self):
        self.text='Score: 10'

window.create_label(ScoreLabel)
```

#### Method 3

```python
score_label = window.create_label(text='Score: 10')
score_label.font_size = 30
```

## User Input

### Keyboard

```python
def on_update(self,dt):
    if window.is_key_pressed(KeyCode.UP):
        self.y += 10

    if window.is_key_down(KeyCode.SPACE):
        self.shoot()

    if window.is_key_up(KeyCode.UP):
        pass
        # We very rarely use this
```

### Mouse

#### Mouse position and delta

```python
window.mouse_position : Point
window.mouse_delta : Point
```

#### Left click events

```python
class Player(Sprite):
    def on_left_click(self):
        """Called when left mouse button is clicked on this sprite."""
        pass


    def on_left_click_anywhere(self):
        """Called when left mouse button is clicked anywhere in the window."""
        pass
```

#### Click events

```python
class Player(Sprite):
    def on_click(self, mouse_event: MouseEvent):
        """Called when ANY mouse button is clicked on this sprite."""
        if mouse_event.button == MouseButton.RIGHT:
            pass

    def on_click_anywhere(self, mouse_event: MouseEvent):
        """Called when ANY mouse button is clicked anywhere in the window."""
        pass
```

## Scheduler

To schedule an action in 1 second (note that the method `self.delete` is not called like ~~`self.delete()`~~)

```python
Scheduler.wait(1, self.delete)
```

To schedule an action to repeat every 2 seconds:

```python
def create_enemy():
    window.create_sprite(Enemy)
Scheduler.update(create_enemy, 2)
```

To cancel a scheduled repeating action:

```python
Scheduler.cancel_update(create_enemy)
```











