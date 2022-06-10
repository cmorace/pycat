from pycat.core import Window, Point
from pycat.base import MouseEvent
from pycat.base.event import KeyEvent


def start_level_editor(w: Window, save_file_path: str):

    class Rect():
        current: 'Rect' = None
        TAG = 'simple.level.editor.rect'

        def __init__(self, top_left: Point):
            self.sprite = w.create_sprite(position=top_left)
            self.sprite.add_tag(Rect.TAG)
            self.sprite.opacity = 100
            self.top_left = top_left

        def set_bottom_right(self, bottom_right: Point):
            d = (self.top_left-bottom_right)
            self.sprite.scale_x = d.x
            self.sprite.scale_y = d.y
            self.sprite.position = bottom_right + d / 2

    def on_mouse_drag(e: MouseEvent):
        if e.button_string == 'Left':
            Rect.current.set_bottom_right(e.position)

    def on_mouse_press(e: MouseEvent):
        if e.button_string == 'Left':
            Rect.current = Rect(e.position)
        elif e.button_string == 'Right':
            Rect.current = None
            rects = w.get_sprites_with_tag(Rect.TAG)
            if rects:
                for r in reversed(rects):
                    if r.contains_point(e.position):
                        r.delete()
                        break

    def on_key_press(e: KeyEvent):
        if e.character == 'f':
            with open(save_file_path, 'a+') as f:
                f.write('from pycat.core import Window\n\n\n')
                f.write('def generate_level(w: Window, tag: str):\n')
                for s in w.get_sprites_with_tag(Rect.TAG):
                    f.write((f'    w.create_sprite'
                             f'(x={s.x},'
                             f' y={s.y},'
                             f' scale_x={s.scale_x},'
                             f' scale_y={s.scale_y},'
                             f' tag=tag)\n'))

    w.subscribe(on_mouse_drag=on_mouse_drag)
    w.subscribe(on_mouse_press=on_mouse_press)
    w.subscribe(on_key_press=on_key_press)


if __name__ == '__main__':
    w = Window()
    start_level_editor(w, 'make_platforms.py')
    w.run()
