from typing import Union, List

from World.Object.Unit.model import Unit
from World.Object.Unit.Player.model import Player

from Utils.Debug.Logger import Logger

from Config.Run.config import Config


class OctreeNode(object):

    MAX_CHILD_NODES = 8

    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'root_node',
        'parent_node',
        'child_nodes',
        'objects',
        'guids'
    )

    def __init__(self, **kwargs):
        self.x0 = kwargs.pop('x0')
        self.x1 = kwargs.pop('x1')
        self.y0 = kwargs.pop('y0')
        self.y1 = kwargs.pop('y1')
        self.z0 = kwargs.pop('z0')
        self.z1 = kwargs.pop('z1')

        self.root_node: OctreeNode = None
        self.parent_node: OctreeNode = None
        self.child_nodes = None

        self.objects = None
        self.guids = None

        # if not self.root_node:
        #     self.nodes_counter = 0
        #     self.total_size = 0
        #     self.without_child = 0

    # https://stackoverflow.com/questions/40049016/using-the-class-as-a-type-hint-for-arguments-in-its-methods
    def get_root_node(self) -> 'OctreeNode':
        return self.root_node

    def set_root_node(self, node: 'OctreeNode') -> None:
        self.root_node = node

    def get_parent_node(self) -> 'OctreeNode':
        return self.parent_node

    def set_parent_node(self, node: 'OctreeNode') -> None:
        self.parent_node = node

    def get_child_nodes(self) -> List['OctreeNode']:
        return self.child_nodes

    def set_child_nodes(self, nodes: List['OctreeNode']) -> None:
        self.child_nodes = nodes

    def can_contain_child_nodes(self) -> bool:
        update_dist = Config.World.Gameplay.update_dist

        return ((self.x1 - self.x0) > update_dist and
                (self.y1 - self.y0) > update_dist and
                (self.z1 - self.z0) > update_dist)

    def get_object(self, guid: int):
        return self.objects.get(guid, None)

    def set_object(self, obj: Union[Unit, Player]) -> None:
        if self.get_child_nodes():
            node = self._get_nearest_child_node(obj)
            node.set_object(obj)
        else:
            self.objects[obj.guid] = obj

    def should_contain_object(self, obj: Union[Unit, Player]) -> bool:
        return (self.x0 <= obj.x <= self.x1 and
                self.y0 <= obj.y <= self.y1 and
                self.z0 <= obj.z <= self.z1)

    def _get_nearest_child_node(self, obj: Union[Unit, Player]):
        for i in range(0, OctreeNode.MAX_CHILD_NODES):
            if self.child_nodes[i].should_contain_object(obj):
                return self.child_nodes[i]
