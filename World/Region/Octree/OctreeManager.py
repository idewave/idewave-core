from typing import Dict

from World.Region.Octree.Builders.OctreeBuilder import OctreeBuilder
from World.Region.Octree.OctreeNode import OctreeNode
from World.Region.Octree.OctreeNodeManager import OctreeNodeManager


class OctreeManager(object):

    @staticmethod
    def create_octree(**kwargs) -> OctreeNode:
        x0: float = kwargs.pop('x0')
        x1: float = kwargs.pop('x1')
        y0: float = kwargs.pop('y0')
        y1: float = kwargs.pop('y1')

        objects: Dict = kwargs.pop('objects')

        builder = OctreeBuilder(x0=x0, x1=x1, y0=y0, y1=y1, objects=objects)
        root_node: OctreeNode = builder.build()

        for obj in objects.values():
            OctreeNodeManager.set_object(root_node, obj)

        return root_node
