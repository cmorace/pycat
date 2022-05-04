import numpy
from pycat.base import NumpyImage

class SpriteSheet:
    def __init__(self, file_name: str, tile_size: int, cell_names=None):
        self.img_array = NumpyImage.get_array_from_file(file_name)
        self.tile_size = tile_size
        self.cell_names = {} if cell_names is None else cell_names

    def update_cell_names(self, new_dict):
        self.cell_names.update(new_dict)

    def get_texture_by_name(self, name: str):
        index = self.cell_names[name]
        return self.get_texture(index[0],index[1])

    def get_texture(self, i: int, j: int, flip_lr: bool = False):
        size = self.tile_size
        cut = self.img_array[                
            j*size : (j+1)*size,
            i*size : (i+1)*size,
            :
        ]

        return NumpyImage.get_texture_from_array(
            numpy.fliplr(cut) if flip_lr else cut)