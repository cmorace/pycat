from typing import List, Optional
from pycat.core import Point
import math

class GridCell:
    def __init__(self, i: int, j: int, center: Point, extents: int):
        self._i: int = i
        self._j: int = j
        self._center: Point = center
        self._extents: int = extents

    @property
    def i(self) -> int:
        return self._i

    @property
    def j(self) -> int:
        return self._j

    @property
    def center(self) -> Point:
        return self._center

    @property
    def extents(self) -> int:
        return self._extents

    @property
    def bottom_left_corner(self) -> Point:
        return Point(self.center.x-self.extents, self.center.y-self.extents)

    @property
    def top_right_corner(self) -> Point:
        return Point(self.center.x+self.extents, self.center.y+self.extents)


class GridLayout:
    def __init__(self, cell_size: int, dims: Point, layout_offset: Point = Point(0,0)):
        self._cell_size = cell_size
        self._extents = int(self._cell_size/2)

        self._layout_offset = layout_offset

        self._dims = dims

        self.cell_array: List[List[GridCell]] = [ [ None for i in range(dims.y) ] for i in range(dims.x) ]
        self.cell_list: List[GridCell] = []
        for i in range(dims.x):
            for j in range(dims.y):
                self.cell_array[i][j] = GridCell(i, j,
                    extents=self._extents,
                    center=Point(
                        self._layout_offset.x + self._extents + i*self._cell_size,
                        self._layout_offset.y + self._extents + j*self._cell_size
                    )                    
                )
                self.cell_list.append(self.cell_array[i][j])

    @property
    def dims(self) -> Point:
        return self._dims

    @property
    def layout_offset(self) -> Point:
        return self._layout_offset

    def __getitem__(self, key):
        return self.cell_array[key]
    
    def get_cells(self) -> List[GridCell]:
        return self.cell_list

    def get_cell_from_position(self, position: Point) -> Optional[GridCell]:
        if (    position.x > self.layout_offset.x 
            and position.y > self.layout_offset.y 
            and position.x < self.layout_offset.x+self._dims.x*self._cell_size
            and position.y < self.layout_offset.y+self._dims.y*self._cell_size
        ):        
            removed_offset = position - self.layout_offset
            i = math.floor(removed_offset.x / self._cell_size)
            j = math.floor(removed_offset.y / self._cell_size)
            return self.cell_array[i][j]
        else:
            return None