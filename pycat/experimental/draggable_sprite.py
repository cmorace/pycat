from pycat.core import Window, Sprite, Point
from pycat.base import MouseEvent


class DraggableSprite(Sprite):
    currently_dragged = None
    top_layer = 0

    def __init__(self, window):
        super().__init__(window)
        self.mouse_offset = Point(0, 0)
        self.layer = DraggableSprite.top_layer
        DraggableSprite.top_layer += 1
        self.is_draggable = True

    @property
    def is_draggable(self) -> bool:
        return self.__is_draggable

    @is_draggable.setter
    def is_draggable(self, is_draggable: bool):
        self.__is_draggable = is_draggable
        if is_draggable:
            self.window.subscribe(on_mouse_drag=self.on_mouse_drag,
                                  on_mouse_release=self.on_mouse_release)
        else:
            self.window.unsubscribe(on_mouse_drag=self.on_mouse_drag,
                                    on_mouse_release=self.on_mouse_release)

    def on_click(self, e: MouseEvent):
        if not self.is_draggable:
            return
        if DraggableSprite.currently_dragged is None:
            DraggableSprite.currently_dragged = self
        elif self.layer > DraggableSprite.currently_dragged.layer:
            DraggableSprite.currently_dragged = self
        self.mouse_offset = self.position - e.position

    def on_mouse_drag(self, e: MouseEvent):
        if self is DraggableSprite.currently_dragged:
            if self.layer < DraggableSprite.top_layer:
                self.layer = DraggableSprite.top_layer
            self.position = e.position + self.mouse_offset

    def on_mouse_release(self, e: MouseEvent):
        if self is DraggableSprite.currently_dragged:
            DraggableSprite.currently_dragged = None
            DraggableSprite.top_layer += 1


if __name__ == '__main__':
    w = Window()

    class Test(DraggableSprite):
        def on_create(self):
            self.scale = 200
            self.set_random_color()

    for i in range(10):
        w.create_sprite(Test, x=300+i*15, y=200+i*25)
    w.run()
