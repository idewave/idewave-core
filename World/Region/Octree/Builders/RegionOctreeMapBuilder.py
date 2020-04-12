from typing import Dict, List

from World.Region.model import Region
from World.Region.Octree.Node import RootNode
from World.Region.Octree.Builders.OctreeBuilder import OctreeBuilder
from World.Object.model import ObjectWithPosition
from Typings.Abstract.AbstractBuilder import AbstractBuilder
from Typings.Constants import REGION_IDENTIFIER


class RegionOctreeMapBuilder(AbstractBuilder):

    def __init__(self, **kwargs):
        self.regions: List[Region] = kwargs.pop('regions')

    def build(self) -> Dict[REGION_IDENTIFIER, RootNode]:
        region_octree_map = {}
        for region in self.regions:
            octree = OctreeBuilder(
                x0=region.x2,
                x1=region.x1,
                y0=region.y2,
                y1=region.y1,
                objects=RegionOctreeMapBuilder._get_objects_with_position(region)
            ).build()

            region_octree_map[region.identifier] = octree

        return region_octree_map

    @staticmethod
    def _get_objects_with_position(region: Region) -> List[ObjectWithPosition]:
        return region.units
