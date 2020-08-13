from pyglet.window import Window as PygletWindow
from pyglet import app
from pycat.geometry.point import Point
from pycat.sprite import Sprite
from pycat.sprite_list import SpriteList
from pycat.label import Label
from pycat.scheduler import Scheduler

from pyglet.clock import schedule_interval as pyglet_schedule_interval
from pyglet.clock import schedule_once as pyglet_schedule_once
from pyglet.clock import unschedule as pyglet_unschedule

class Window():

    def __init__(
        self, 
        width: int = 1280, 
        height:int = 640, 
        background_image='',
        enforce_window_limits=True
    ):
        self.__window: PygletWindow = PygletWindow(width,height)

        self.__active_keys: Set[int] = set()
        self.__window.on_key_press = self.__on_key_press
        self.__window.on_key_release = self.__on_key_release
        self.__user_key_press = lambda key,mod: None
        self.__user_key_release = lambda key,mod: None
        

        self.__window.on_draw = self.__auto_draw
        
        self.__enforce_window_limits = enforce_window_limits
        self.__pre_draw_function = lambda: None
        self.__post_draw_function = lambda: None

        # First element of __sprite_lists reserved for Sprites directly added to the window.
        # Remainder of list contains SpriteLists that were added by user.
        self.__sprite_lists: [SpriteList] = [SpriteList()]

        self.__labels: [label] = []

        self.__background_sprite = None
        if background_image:
            self.__background_sprite = Sprite(background_image)
            self.__background_sprite.position = self.get_center()


    # Sprite / Label management

    def add_label(self, label: Label):
        self.__labels.append(label)

    def add_sprite_list(self, sprite_list: SpriteList):
        self.__sprite_lists.append(sprite_list)

    def add_sprite(self, sprite: Sprite):
        self.__sprite_lists[0].add(sprite)
        
    def remove_sprite(self, sprite: Sprite):
        self.__sprite_lists[0].remove(sprite)


    # Drawing

    def clear(self):
        self.__window.clear()

    def set_pre_draw(self, pre_draw_function):
        self.__pre_draw_function = pre_draw_function

    def set_post_draw(self, post_draw_function):
        self.__post_draw_function = post_draw_function

    def __auto_draw(self):

        self.clear()

        self.__pre_draw_function()

        if self.__background_sprite:
            self.__background_sprite.draw()
        
        all_sprites = SpriteList.flatten_sprite_lists(self.__sprite_lists)

        if self.__enforce_window_limits:
            for s in all_sprites:
                s.limit_position_to_area(0, self.width, 0, self.height)

        objects_to_draw = all_sprites + self.__labels
        objects_to_draw.sort(key=lambda o: o.layer)

        for o in objects_to_draw:
            o.draw()       

        self.__post_draw_function() 


    # Key input

    def is_active_key(self, keycode: int) -> bool:
        return keycode in self.__active_keys

    def set_on_key_press(self, key_press_function):
        self.__user_key_press = key_press_function

    def set_on_key_release(self, key_release_function):
        self.__user_key_release = key_release_function

    def __on_key_press(self, key, mod):
        self.__user_key_press(key,mod)
        self.__active_keys.add(key)

    def __on_key_release(self, key, mod):
        self.__user_key_release(key,mod)
        self.__active_keys.remove(key)

    # Runtime

    def run(self):
        app.run()

    
    # Helpers

    def get_center(self) -> Point:
        return Point(self.width/2, self.height / 2)


    # Properties

    @property
    def width(self) -> int:
        size: Tuple = self.__window.get_size()
        return size[0]

    @property
    def height(self) -> int:
        size: Tuple = self.__window.get_size()
        return size[1]    

    

    


