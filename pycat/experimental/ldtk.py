from typing import List, Tuple, Optional
from pycat.core import Point, Sprite, Color, Window
from pycat.base import NumpyImage
import json
from .ldtk_parser import ldtk_from_dict, TilesetDefinition, Level, LayerInstance

class LdtkLevelNotFoundException(Exception):
    def __init__(self, level_name: str, ldtk_file: str):
        self.level_name = level_name
        self.ldtk_file = ldtk_file

    def __str__(self):
        return 'Level "'+self.level_name+'" not found in Ldtk file "'+self.ldtk_file+'"'

class LdtkTagTile:
    def __init__(self, center: Point, size: int, value: int, tag: str, color: str):
        self._center = center
        self._size = size
        self._value = value
        self._tag = tag
        self._color = color

    @property
    def center(self) -> Point:
        return self._center

    @property
    def size(self) -> int:
        return self._size

    @property
    def value(self) -> int:
        return self._value

    @property
    def tag(self) -> str:
        return self._tag

    @property
    def color(self) -> Color:
        return Color.hex(self._color)
    

class LdtkImageTile:
    def __init__(self, px: Point, src: Point, tileset: TilesetDefinition, level: Level, layer_idx: int, ldtk_file: 'LdtkFile'):
        self._px = px
        self._src = src
        self._tileset = tileset
        self._level = level
        self._layer_idx = layer_idx
        self._ldtk_file = ldtk_file
        self._tile_size = self._tileset.tile_grid_size

    @property
    def center(self) -> Point:
        extents = int(self._tileset.tile_grid_size/2)
        return Point(
            self._px.x + extents, 
            self._level.px_hei - self._tile_size - self._px.y + extents
        )

    @property
    def tileset_bottom_left_corner(self) -> Point:
        return Point(
            self._src.x,
            self._tileset.px_hei - self._tile_size - self._src.y
        )

    @property
    def tileset_top_right_corner(self) -> Point:
        return self.tileset_bottom_left_corner + Point(self._tile_size, self._tile_size)

    @property
    def layer(self) -> int:
        return self._layer_idx

    def get_texture(self):
        tileset_image = self._ldtk_file._tileset_images[self._tileset.rel_path]

        segment = tileset_image[
            self.tileset_bottom_left_corner.y : self.tileset_top_right_corner.y,
            self.tileset_bottom_left_corner.x : self.tileset_top_right_corner.x
            :
        ]

        return NumpyImage.get_texture_from_array(segment) 
 
            
class LdtkFile:
    def __init__(self,ldtk_file: str):
        self._ldtk_file = ldtk_file
        json_string = open(ldtk_file,'r').read()
        self._data = ldtk_from_dict(json.loads(json_string))

        self._tileset_images = {
            ts.rel_path: NumpyImage.get_array_from_file(ts.rel_path) 
            for ts in self._data.defs.tilesets
        }


    def render_level(
        self, 
        window: Window, 
        level_name: str, 
        debug_tags: bool = False, 
        debug_layer: int = 1000,
        debug_font_size: int = 10
    ) -> None:
        
        for image_tile in self.get_image_tiles_for_level(level_name):
            tile = window.create_sprite(
                position=image_tile.center, 
                layer=image_tile.layer,
                texture=image_tile.get_texture() )

        for tag_tile in self.get_tag_tiles_for_level(level_name):
            tile = window.create_sprite(
                position=tag_tile.center, 
                scale=tag_tile._size, 
                layer=debug_layer,
                opacity=100 if debug_tags else 0,
                tag=tag_tile.tag,
                color=tag_tile.color)
            if debug_tags:
                label = window.create_label(
                    text=tag_tile.tag,
                    position=tile.position,
                    layer=debug_layer+1,
                    font_size=debug_font_size
                )
                label.y += label.content_height/2
                label.x -= label.content_width/2


    def get_level(self, level_name: str) -> Optional[Level]:
        try:
            [level] = (level for level in self._data.levels if level.identifier == level_name)
            return level
        except ValueError:
            raise LdtkLevelNotFoundException(level_name, self._ldtk_file)
        

    def get_image_tiles_for_level(self, level_name: str) -> List[LdtkImageTile]:
        level = self.get_level(level_name)

        image_tiles = []

        layer_instance: LayerInstance
        # level.layer_instances are stored in order from top to bottom layer, hence the reversed()
        for layer_idx, layer_instance in enumerate(reversed(level.layer_instances)):

            if layer_instance.type == 'Tiles':

                [tileset] = (tileset for tileset in self._data.defs.tilesets
                    if tileset.uid == layer_instance.tileset_def_uid)

                for tile in layer_instance.grid_tiles:

                    image_tiles.append(
                        LdtkImageTile(
                            Point(tile.px[0], tile.px[1]), 
                            Point(tile.src[0], tile.src[1]), 
                            tileset,
                            level,
                            layer_idx,
                            self))

        return image_tiles


    def get_tag_tiles_for_level(self, level_name: str) -> List[LdtkTagTile]:
        level = self.get_level(level_name)

        tag_tiles = []

        for layer_instance in level.layer_instances:

            if layer_instance.type == 'IntGrid':

                [layer_def] = (layer for layer in self._data.defs.layers
                    if layer.uid == layer_instance.layer_def_uid)

                int_to_id_map = {pair.value: pair.identifier for pair in layer_def.int_grid_values}
                int_to_color_map = {pair.value: pair.color for pair in layer_def.int_grid_values}
                
                height = layer_instance.c_hei
                width = layer_instance.c_wid
                size = layer_instance.grid_size
                extents = int(size*0.5)
                csv = layer_instance.int_grid_csv

                for i in range(width):
                    for j in range(height):
                        csv_idx = j*width + i
                        csv_val = csv[csv_idx]
                        if csv_val != 0:
                            tag_tiles.append(
                                LdtkTagTile(
                                    Point(i*size+extents,height*size-j*size-extents),
                                    size,
                                    csv_val,
                                    int_to_id_map[csv_val],
                                    int_to_color_map[csv_val]
                                )
                            )

        return tag_tiles