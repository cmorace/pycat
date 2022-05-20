import numpy
from pycat.base import NumpyImage


class SpriteSheet:
    def __init__(self, file_name: str, tile_size_x: int, tile_size_y: int, cell_names=None):
        self.img_array = NumpyImage.get_array_from_file(file_name)
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        self.cell_names = {} if cell_names is None else cell_names

    def update_cell_names(self, new_dict):
        self.cell_names.update(new_dict)

    def get_texture_by_name(self, name: str):
        index = self.cell_names[name]
        return self.get_texture(index[0],index[1])

    def get_textures_by_pattern(self, pattern: str):
        name_map_sorted = sorted(self.cell_names.items(), key=lambda kvp: kvp[0])
        return [
            self.get_texture(index[0],index[1]) 
            for name,index in name_map_sorted
            if pattern in name
        ]

    def get_texture(self, i: int, j: int, flip_lr: bool = False):
        cut = self.img_array[                
            j * self.tile_size_y : (j+1) * self.tile_size_y,
            i * self.tile_size_x : (i+1) * self.tile_size_x,
            :
        ]

        return NumpyImage.get_texture_from_array(
            numpy.fliplr(cut) if flip_lr else cut)


class UniversalLPCSpritesheet(SpriteSheet):
    # Loads sprites created with
    # https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator

    def __init__(self, file_name: str):
        super().__init__(file_name, 64, 64)
        self.update_cell_names( {'hurt_'+str(i):        (i,0) for i in range(6) })

        self.update_cell_names( {'shoot_right_'+str(i): (i,1) for i in range(13) })
        self.update_cell_names( {'shoot_down_'+str(i):  (i,2) for i in range(13) })
        self.update_cell_names( {'shoot_left_'+str(i):  (i,3) for i in range(13) })
        self.update_cell_names( {'shoot_up_'+str(i):    (i,4) for i in range(13) })

        self.update_cell_names( {'slash_right_'+str(i): (i,5) for i in range(6) })
        self.update_cell_names( {'slash_down_'+str(i):  (i,6) for i in range(6) })
        self.update_cell_names( {'slash_left_'+str(i):  (i,7) for i in range(6) })
        self.update_cell_names( {'slash_up_'+str(i):    (i,8) for i in range(6) })      

        # first frame of walk is idle
        self.update_cell_names( {'idle_right_'+str(i):  (i,9) for i in range(0,1) })
        self.update_cell_names( {'idle_down_'+str(i):   (i,10) for i in range(0,1) })
        self.update_cell_names( {'idle_left_'+str(i):   (i,11) for i in range(0,1) })
        self.update_cell_names( {'idle_up_'+str(i):     (i,12) for i in range(0,1) })    

        # remaining frames of walk cycle
        self.update_cell_names( {'walk_right_'+str(i):  (i,9) for i in range(1,9) })
        self.update_cell_names( {'walk_down_'+str(i):   (i,10) for i in range(1,9) })
        self.update_cell_names( {'walk_left_'+str(i):   (i,11) for i in range(1,9) })
        self.update_cell_names( {'walk_up_'+str(i):     (i,12) for i in range(1,9) })          

        self.update_cell_names( {'smash_right_'+str(i): (i,13) for i in range(8) })
        self.update_cell_names( {'smash_down_'+str(i):  (i,14) for i in range(8) })
        self.update_cell_names( {'smash_left_'+str(i):  (i,15) for i in range(8) })
        self.update_cell_names( {'smash_up_'+str(i):    (i,16) for i in range(8) })            

        self.update_cell_names( {'cast_right_'+str(i):  (i,17) for i in range(7) })
        self.update_cell_names( {'cast_down_'+str(i):   (i,18) for i in range(7) })
        self.update_cell_names( {'cast_left_'+str(i):   (i,19) for i in range(7) })
        self.update_cell_names( {'cast_up_'+str(i):     (i,20) for i in range(7) })                    

        # Steal a frame from cast to use as a single frame jump
        self.update_cell_names( {'jump_right_'+str(i):  (i,17) for i in range(4,5) })
        self.update_cell_names( {'jump_down_'+str(i):   (i,18) for i in range(4,5) })
        self.update_cell_names( {'jump_left_'+str(i):   (i,19) for i in range(4,5) })
        self.update_cell_names( {'jump_up_'+str(i):     (i,20) for i in range(4,5) })                