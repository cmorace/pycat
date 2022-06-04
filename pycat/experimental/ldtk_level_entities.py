import json
from dataclasses import dataclass
from typing import List

from pycat.debug import print_warning
from pycat.experimental.ldtk_parser import ImageExportMode, ldtk_from_dict


@dataclass
class Entity:
    id: str
    x: float
    y: float
    width: float
    height: float
    tags: List[str]


@dataclass
class LevelData:
    id: str
    x: float
    y: float
    width: float
    height: float
    entities: List[Entity]


def get_levels_entities(ldtk_file_path: str) -> List[LevelData]:
    json_string = open(ldtk_file_path, 'r').read()
    data = ldtk_from_dict(json.loads(json_string))
    level_data = []
    for level in data.levels:
        entities = []
        for layer in level.layer_instances:
            for e in layer.entity_instances:
                entities.append(
                    Entity(
                        e.identifier,
                        e.px[0] + e.width/2,
                        level.px_hei-e.px[1] - e.height/2,
                        e.width,
                        e.height,
                        e.tags)
                )
        level_data.append(
            LevelData(
                level.identifier,
                level.world_x,
                level.world_y,
                level.px_wid,
                level.px_hei,
                entities)
        )
    if data.image_export_mode is not ImageExportMode.ONE_IMAGE_PER_LEVEL:
        print_warning('export level as a single image (in Project Settings')
    return level_data
