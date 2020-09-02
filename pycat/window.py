from pyglet.window import Window as PygletWindow
from pyglet import app

from pyglet.clock import schedule_interval as pyglet_schedule_interval
from pyglet.clock import schedule_once as pyglet_schedule_once
from pyglet.clock import unschedule as pyglet_unschedule

from pyglet.window.mouse import LEFT as LEFT_MOUSE_BUTTON

from pycat.geometry.point import Point
from pycat.geometry.region import point_in_region
from pycat.sprite import Sprite, UnmanagedSprite
from pycat.label import Label
from pycat.scheduler import Scheduler


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

        self.__window.on_mouse_press = self.__on_mouse_press
        
        self.__mouse_position = Point(0,0)
        self.__mouse_delta = Point(0,0)
        self.__window.on_mouse_motion = self.__on_mouse_motion

        self.__window.on_draw = self.__auto_draw
        
        self.__enforce_window_limits = enforce_window_limits
        self.__pre_draw_function = lambda: None
        self.__post_draw_function = lambda: None

        # First element of __sprite_lists reserved for Sprites directly added to the window.
        # Remainder of list contains SpriteLists that were added by user.
        self.__sprites: [Sprite] = []
        self.__tagmap = {}

        self.__labels: [Label] = []

        self.__background_sprite = None
        if background_image:
            self.set_background_image(background_image)


    # Sprite / Label management

    def add_label(self, label: Label):
        self.__labels.append(label)

    def create_sprite(self, sprite_cls=Sprite):
        sprite = sprite_cls(window=self)
        self.__register_sprite(sprite)
        return sprite

    def create_sprite_with_tag(self, sprite_cls, tag):
        sprite = sprite_cls(window=self, tags=[tag])
        self.__register_sprite(sprite)
        return sprite        

    def create_sprite_with_tags(self, sprite_cls, tags):
        sprite = sprite_cls(window=self, tags=tags)
        self.__register_sprite(sprite)
        return sprite    

    def delete_sprite(self, sprite):
        self.__deregister_sprite(sprite)

    def delete_sprites_with_tag(self, tag):
        # this could be optimized
        for sprite in self.__tagmap.get(tag,[]):            
            self.__deregister_sprite(sprite)
        # leaves tag in __tagmap 

    def __register_sprite(self, sprite):
        self.__sprites.append(sprite)
        for tag in sprite.get_tags():
            if tag not in self.__tagmap:
                self.__tagmap[tag] = []
            self.__tagmap[tag].append(sprite)

        sprite.on_create()
        pyglet_schedule_interval(sprite.on_update, 1/60)            

    def __deregister_sprite(self, sprite):
        pyglet_unschedule(sprite.on_update)
        
        self.__sprites.remove(sprite)
        for tag,sprites in self.__tagmap.items():
            if sprite in sprites:
                self.__tagmap[tag] = [s for s in self.__tagmap[tag] if s is not sprite]

    def get_sprites_with_tag(self, tag):
        return self.__tagmap.get(tag, [])


    # Drawing

    def clear(self):
        self.__window.clear()

    def set_background_image(self, image):
        self.__background_sprite = UnmanagedSprite(self)
        self.__background_sprite.image = image
        self.__background_sprite.position = self.get_center()

    def set_pre_draw(self, pre_draw_function):
        self.__pre_draw_function = pre_draw_function

    def set_post_draw(self, post_draw_function):
        self.__post_draw_function = post_draw_function

    def __auto_draw(self):

        self.clear()

        self.__pre_draw_function()

        if self.__background_sprite:
            self.__background_sprite.draw()

        if self.__enforce_window_limits:
            for s in self.__sprites:
                s.limit_position_to_area(0, self.width, 0, self.height)

        objects_to_draw = self.__sprites + self.__labels
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
        if key in self.__active_keys:
            self.__active_keys.remove(key)


    # Mouse input

    def __on_mouse_motion(self, x, y, dx, dy):
        self.__mouse_position.x = x
        self.__mouse_position.y = y
        self.__mouse_delta.x = dx
        self.__mouse_delta.y = dy


    def __on_mouse_press(self, x, y, button, modifiers):

        for sprite in self.__sprites:

            llc = Point(sprite.position.x - sprite.width/2, sprite.position.y - sprite.height/2)
            urc = Point(sprite.position.x + sprite.width/2, sprite.position.y + sprite.height/2)

            if point_in_region(
                lower_left_corner = llc,
                upper_right_corner = urc,
                x = x,
                y = y
            ):
                sprite.on_click(x,y,button,modifiers)
                if button == LEFT_MOUSE_BUTTON:
                    sprite.on_left_click()


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

    @property
    def mouse_position(self) -> Point:
        return self.__mouse_position

    @property
    def mouse_delta(self) -> Point:
        return self.__mouse_delta
    

    


