"""forked from pycat.window to do some testing"""
from threading import Lock
from typing import Callable, Dict, List, Optional, Set, Type, Protocol

from pycat.base.event.key_event import KeyEvent
from pycat.base.sprite import Sprite as BaseSprite
from pycat.base.window import Window as BaseWindow
from pycat.scheduler import Scheduler

class GameObject(Protocol):

    def __init__(self, window: 'Window', tags: List[str]):...
    
    @property
    def tags(self) -> List[str]:...
    
    @property
    def layer(self) -> int:...

    @property
    def is_deleted(self) -> bool:...

    def draw(self):...

    def on_update(self, dt: float):...


    

class SpriteCreationError(Exception):
    pass

class Window(BaseWindow):

    def __init__(
        self, 
        width: int = 1280, 
        height:int = 640, 
        background_image: str ='',
        title: str = ""
    ):
        super().__init__(width, height, title)

        self.__background_sprite: Optional[BaseSprite] = None
        if background_image:
            self.set_background_image(background_image)
                
        self.__keys_lock = Lock()
        self.__keys_async: Set[int] = set()
        self.__keys_down_async: Set[int] = set()
        self.__keys_up_async: Set[int] = set()

        self.__keys: Set[int] = set()
        self.__keys_down: Set[int] = set()
        self.__keys_up: Set[int] = set()

        self.add_event_listeners(on_key_press=self.__on_key_press,
                                 on_key_release=self.__on_key_release)

        self.__game_objects: List[GameObject] = []
        self.__tagmap: Dict[str, List[GameObject]] = {}
        
        self.__pre_draw: Optional[Callable[[None], None]] = None
        self.on_draw(self.__auto_draw)
        self.__post_draw: Optional[Callable[[None], None]] = None

    def create_game_object(self, cls: Type[GameObject], tags: Optional[List[str]]):
        game_object = cls(self, tags or [])
        self.add_game_object(game_object)
        return game_object

    # Sprite / Label management
    def add_game_object(self, game_object: GameObject):
        self.__game_objects.append(game_object)
        for tag in game_object.tags:
            if tag not in self.__tagmap:
                self.__tagmap[tag] = []
            self.__tagmap[tag].append(game_object)
        self.__update_draw_list()

    def delete_game_object(self, drawable: GameObject):
        self.__deregister_game_object(drawable)
        self.__update_draw_list()

    def delete_game_objects_with_tag(self, tag):
        # this could be optimized
        for sprite in self.__tagmap.get(tag,[]):            
            self.__deregister_game_object(sprite)
        # leaves tag in __tagmap
        self.__update_draw_list()


    def __deregister_game_object(self, game_object: GameObject):        
        self.__game_objects.remove(game_object)
        for tag, game_objects in self.__tagmap.items():
            if game_object in game_objects:
                self.__tagmap[tag] = [s for s in self.__tagmap[tag] 
                                         if s is not game_object]

    def get_game_object_with_tag(self, tag):
        return self.__tagmap.get(tag, [])

    def get_all_game_objects(self):
        return self.__draw

    def dump_all_game_objects(self):
        return 'Drawable in window: \n\t'+'\n\t'.join([str(s) 
                for s in self.__game_objects])

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

    def __auto_draw(self):
        
        self.clear()

        if self.__pre_draw:
            self.__pre_draw()

        if self.__background_sprite:
            self.__background_sprite.draw()

        # @todo: add batch rendering
        # still need to implement layers 
        # using pyglet.graphics.OrderedGroup
        for o in self.__game_objects:
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


        # I think there was a bug here previously,
        # if a sprite deletes itself during its own update function 
        # then self.__sprites will be modified while iterating
        # I added the code below and changed the sprite's delete method
        for s in self.__game_objects:
            s.on_update(dt)
            

        # I changed the sprite class's delete() function to set a flag
        # if it wants to delete itself (sprite._is_self_deleted == True)
        # then we delete the sprites after update if needed
        # --------------------------
        needs_update = False
        for s in self.__game_objects:
            if s.is_deleted:
                needs_update = True
                for tag in s.tags:
                    self.__tagmap[tag].remove(s)
        if needs_update:
            self.__game_objects = [s for s in self.__game_objects if not s.is_deleted]
            self.__update_draw_list()
        # -------------------  


    def __update_draw_list(self):
        """Call when we add or remove objects to draw"""
        self.__game_objects.sort(key=lambda o: o.layer)


    def run(self, **kwargs):
        Scheduler.update(self.__game_loop)
        super().run(**kwargs)

