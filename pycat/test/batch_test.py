"""This is a test to check batch rendering and event handling performance.

The class `pycat.base.Sprite` now inherits from the `WindowEventListener`
calss and can receive any window event by overriding a set of methods
and adding the sprite to a window using the
`window.add_window_event_listener(s: WindowEventListener)` method.
In order to be collected by the garbage collector, they must also
be removed using the
`window.remove_window_event_listener(s: WindowEventListener)`. Events are
handled by the `WindowEventHandler` class using a publisher subscriber model.

The frames per second are displayed on the window. Garbage collection is
tested using print statements in the custom sprites `__del__` method and
python's `gc` module

Tests:
- Press the `enter` key to generate 1000 sprites listening for window events.
  You can do this multiple times.
- Press the `0` key to delete all of the generated sprites
- Press backspace to delete one by one
- Right click to remove all sprites under the mouse cursor
- Press the other number keys to change their opacity
- Mouse motion changes the sprites orientation
- Mouse drag will change the color of sprites under the mouse cursor
 """

import gc
from random import uniform
from typing import List

from pycat.base.event.key_event import KeyCode, KeyEvent
from pycat.base.event.mouse_event import MouseButton, MouseEvent
from pycat.base.graphics_batch import GraphicsBatch
from pycat.base.image import Image
from pycat.base.base_sprite import BaseSprite
from pycat.base.base_window import BaseWindow
from pycat.geometry.point import Point
from pycat.collision import is_aabb_collision, is_rotated_box_collision

# gc.set_debug(gc.DEBUG_STATS)


class Eye(BaseSprite):
    """Our test Sprite.

    Inherits from `pycat.base.Sprite`
    """
    def __init__(self, look_point: Point, max_x: float, max_y: float):
        super().__init__(Image.get_image_from_file("img/eye.png"))
        self.scale = uniform(0.1, 0.3)
        self.goto_random_position(max_x=max_x, max_y=max_y)
        self.point_toward(look_point)
        self.shake = False

    # for testing garbage collection
    def __del__(self):
        # print("Eye garbage collected")
        pass

    def on_key_press(self, key_event: KeyEvent):
        if key_event.character.isnumeric():
            self.opacity = 28 * int(key_event.character)

    def on_mouse_motion(self, e: MouseEvent):
        self.point_toward(e.position)

    def on_mouse_press(self, e: MouseEvent):
        if self.contains_point(e.position):
            self.shake = not self.shake

    def update(self):
        if self.shake:
            self.x += uniform(-1, 1)
            self.y += uniform(-1, 1)
            self.scale *= uniform(0.98, 1.02)


window = BaseWindow(500, 500, "window events test")
flappy_bird = BaseSprite(Image.get_image_from_file("img/bird_cropped.gif"))
flappy_bird.position = window.center
flappy_bird.scale = 0.4
sprite_list: List[Eye] = []
eye_batch = GraphicsBatch()


def delete_eyes():
    for s in sprite_list:
        window.remove_event_subscriber(s)
    sprite_list.clear()
    eye_batch.clear()


def my_key_press(event: KeyEvent):
    if event == KeyCode.ENTER:
        for _ in range(1000):
            s = Eye(look_point=flappy_bird.position,
                    max_x=window.width,
                    max_y=window.height)
            sprite_list.append(s)
            eye_batch.add_sprite(s)
            window.add_event_subscriber(s)
        flappy_bird.set_image_from_file("img/bird_cropped.gif")
        flappy_bird.color = (255, 255, 255)
    if event.symbol == KeyCode.BACKSPACE and sprite_list:
        s = sprite_list.pop()
        eye_batch.remove_sprite(s)
        window.remove_event_subscriber(s)
    elif event == "0":
        flappy_bird.set_image_from_file("img/boom.png")
        flappy_bird.scale = 0.5
        flappy_bird.position = window.center
        flappy_bird.color = (255, 255, 255)
        delete_eyes()
    elif event == "r":
        flappy_bird.color = (255, 0, 0)
    elif event == "g":
        flappy_bird.color = (0, 255, 0)
    elif event == "b":
        flappy_bird.color = (0, 0, 255)


def my_mouse_scroll(mouse: MouseEvent):
    """zoom flappy bird"""
    if mouse.delta.y < 0 and flappy_bird.scale < 3:
        flappy_bird.scale *= 1 - mouse.delta.y / 10
    elif mouse.delta.y > 0 and flappy_bird.scale > 0.1:
        flappy_bird.scale *= 1 - mouse.delta.y / 10


def my_mouse_drag(mouse: MouseEvent):
    """drag flappy bird"""
    if (flappy_bird.contains_point(mouse.position)
            or flappy_bird.contains_point(mouse.position - mouse.delta)):
        flappy_bird.position = mouse.position
        for s in sprite_list:
            if is_aabb_collision(flappy_bird, s):
                s.color = (255, 0, 0)


def my_mouse_press(mouse: MouseEvent):
    if mouse.button == MouseButton.RIGHT:
        remove_list: List[BaseSprite] = []
        for s in sprite_list:
            if s.contains_point(mouse.position):
                remove_list.append(s)
        for s in remove_list:
            window.remove_event_subscriber(s)
            sprite_list.remove(s)
            eye_batch.remove_sprite(s)


def test_key_press(event: KeyEvent):
    print("press", event)


def test_key_release(event: KeyEvent):
    print("release", event)


@window.on_update
def update():
    if window.is_active_key(KeyCode.UP):
        flappy_bird.rotation += 3
    elif window.is_active_key(KeyCode.DOWN):
        flappy_bird.rotation -= 3
    elif window.is_active_key(KeyCode.RIGHT):
        flappy_bird.change_animation_frame_duration(-0.002)
    elif window.is_active_key(KeyCode.LEFT):
        flappy_bird.change_animation_frame_duration(0.002)
    for s in sprite_list:
        s.update()
    window._fps_label.update()


@window.on_draw
def draw():
    window.clear()
    eye_batch.draw()
    flappy_bird.draw()
    window._fps_label.draw()


window.run(on_key_press=[my_key_press, test_key_press],
           on_key_release=test_key_release,
           on_mouse_press=my_mouse_press,
           on_mouse_scroll=my_mouse_scroll,
           on_mouse_drag=my_mouse_drag)
