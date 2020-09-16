from threading import Lock
from typing import Callable, Dict, List, Optional, Set, Type, Union

from pycat.base.event.key_event import KeyEvent
from pycat.base.event.mouse_event import MouseButton, MouseEvent
from pycat.base.sprite import Sprite as BaseSprite
from pycat.base.window import Window as BaseWindow
from pycat.label import Label
from pycat.scheduler import Scheduler
from pycat.sprite import Sprite


class SpriteCreationError(Exception):
    pass

class Window(BaseWindow):

    def __init__(
        self, 
        width: int = 1280, 
        height:int = 640, 
        background_image: str ='',
        enforce_window_limits: bool =True,
        title: str = ""
    ):
        super().__init__(width, height, title)

        self.__background_sprite: Optional[BaseSprite] = None
        if background_image:
            self.set_background_image(background_image)
        
        self.__enforce_window_limits = enforce_window_limits
        
        self.__keys_lock = Lock()
        self.__keys_async: Set[int] = set()
        self.__keys_down_async: Set[int] = set()
        self.__keys_up_async: Set[int] = set()

        self.__keys: Set[int] = set()
        self.__keys_down: Set[int] = set()
        self.__keys_up: Set[int] = set()

        self.add_event_listeners(on_key_press=self.__on_key_press,
                                 on_key_release=self.__on_key_release,
                                 on_mouse_press=self.__on_mouse_press)

        self.__sprites: List[Sprite] = []
        self.__tagmap: Dict[str, List[Sprite]] = {}
        self.__labels: List[Label] = []
        self.__objects_to_draw: List[Union[Sprite, Label]] = []
        
        self.__pre_draw: Optional[Callable[[None], None]] = None
        self.on_draw(self.__auto_draw)
        self.__post_draw: Optional[Callable[[None], None]] = None
        

    # Sprite / Label management

    def add_label(self, label: Label):
        self.__labels.append(label)
        self.__update_draw_list()


    def create_sprite(self, sprite_cls: Type[Sprite]=Sprite, **kwargs):
        # Sanity check kwargs
        for arg_name in kwargs:
            if arg_name not in ['tag', 'tags', 'image', 'x', 'y', 'scale']:
                raise SpriteCreationError("You may not set '"+arg_name+"' when creating a sprite")

        if 'tag' in kwargs and 'tags' in kwargs:
            raise SpriteCreationError("You may not specify both 'tag' and 'tags'" "when creating a sprite")

        # Create a class
        tags = kwargs.pop('tags', [])
        if 'tag' in kwargs:
            tags += kwargs.pop('tag')
        sprite = sprite_cls(window=self,tags=tags)

        # Store references in the window
        self.__sprites.append(sprite)        
        for tag in sprite.tags:
            if tag not in self.__tagmap:
                self.__tagmap[tag] = []
            self.__tagmap[tag].append(sprite)

        # Call on_create and override kwargs
        sprite.on_create()
        for arg_name, arg_value in kwargs.items():
            setattr(sprite, arg_name, arg_value)     
        self.__update_draw_list()
        return sprite

    # there was a bug here,
    # we can't delete while we are iterating over the sprite list in update
    def delete_sprite(self, sprite):
        # self.__deregister_sprite(sprite)
        sprite.delete()

    def delete_sprites_with_tag(self, tag):
        # this could be optimized
        for sprite in self.__tagmap.get(tag,[]): 
            sprite.delete()           
            #self.__deregister_sprite(sprite)
        # leaves tag in __tagmap

    # def __deregister_sprite(self, sprite):        
    #     self.__sprites.remove(sprite)
    #     for tag, sprites in self.__tagmap.items():
    #         if sprite in sprites:
    #             self.__tagmap[tag] = [s for s in self.__tagmap[tag] 
    #                                      if s is not sprite]

    def get_sprites_with_tag(self, tag):
        return self.__tagmap.get(tag, [])

    def get_all_sprites(self):
        return self.__sprites

    def dump_all_sprites(self):
        return 'Sprites in window: \n\t'+'\n\t'.join([str(s) 
                for s in self.__sprites])

    # Drawing

    def set_background_image(self, image: str):
        if self.__background_sprite is not None:
            self.__background_sprite.image = image
        else:
            c = self.center
            b = BaseSprite.create_from_file(image, c.x, c.y, 0)
            self.__background_sprite = b
            self.__background_sprite.position = c

    def set_pre_draw(self, pre_draw_func: Callable[[None], None]):
        self.__pre_draw = pre_draw_func

    def set_post_draw(self, post_draw_func: Callable[[None], None]):
        self.__post_draw = post_draw_func

    # I think we should minimize computation in the draw function
    # so I moved bounds checking to the update function 
    # and only update drawable objects when we add or remove them
    def __auto_draw(self):
        
        self.clear()

        if self.__pre_draw:
            self.__pre_draw()

        if self.__background_sprite:
            self.__background_sprite.draw()

        # @todo: add batch rendering
        # still need to implement layers 
        # using pyglet.graphics.OrderedGroup
        for o in self.__objects_to_draw:
            o.draw()

        if self.__post_draw:
            self.__post_draw()


    # Key input

    def get_key(self, keycode: int) -> bool:
        return keycode in self.__keys

    def get_key_down(self, keycode: int) -> bool:
        return keycode in self.__keys_down

    def get_key_up(self, keycode: int) -> bool:
        return keycode in self.__keys_up

    def __on_key_press(self, e: KeyEvent):
        with self.__keys_lock:
            self.__keys_down_async.add(e.symbol)
            self.__keys_async.add(e.symbol)        

    def __on_key_release(self, e: KeyEvent):
        with self.__keys_lock:
            self.__keys_up_async.add(e.symbol)
            if e.symbol in self.__keys_async:
                self.__keys_async.remove(e.symbol)
            
    # Mouse input

    def __on_mouse_press(self, e: MouseEvent):
        p = e.position
        for sprite in self.__sprites:
            if sprite.contains_point(p):
                sprite.on_click(e)
                if e.button == MouseButton.LEFT:
                    sprite.on_left_click()

    # Runtime

    def __game_loop(self, dt: float):

        # ensure key tests performed during on_updates this frame 
        # all see the same set of keys (and keys up/down)
        with self.__keys_lock:
            self.__keys = self.__keys_async.copy()
            
            # consume keys down
            self.__keys_down = self.__keys_down_async.copy()
            self.__keys_down_async.clear()

            # consume keys up
            self.__keys_up = self.__keys_up_async.copy()
            self.__keys_up_async.clear()


        # There was a bug here previously,
        # if a sprite deletes itself during its own update function 
        # then self.__sprites will be modified while iterating
        # so we need to update then delete

        # save a little time by checking window limits outside loop
        if self.__enforce_window_limits:
            for s in self.__sprites:
                s.on_update(dt)
                s.limit_position_to_area(0, self.width, 0, self.height)
        else:
            for s in self.__sprites:
                s.on_update(dt)

        # I changed the sprite class's delete() function to set a flag
        # (sprite._is_deleted == True)
        # first we update then we delete sprites
        # --------------------------
        # check if any sprites were deleted
        # prevent unecessary copy and sort
        removables = [s for s in self.__sprites if s.is_deleted]
        if removables:
            for s in removables:
                for tag in s.tags:
                    self.__tagmap[tag].remove(s)
            self.__sprites = [s for s in self.__sprites if not s.is_deleted]
            self.__update_draw_list()
        # -------------------  


    def __update_draw_list(self):
        """Call when we add objects to draw"""
        self.__objects_to_draw = self.__sprites + self.__labels
        self.__objects_to_draw.sort(key=lambda o: o.layer)


    def run(self, **kwargs):
        Scheduler.update(self.__game_loop)
        super().run(**kwargs)

