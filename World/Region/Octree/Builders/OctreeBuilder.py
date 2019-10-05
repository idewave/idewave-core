from typing import Union, Dict, List

from World.Object.Unit.model import Unit
from World.Object.Unit.Player.model import Player

from World.Region.Octree.OctreeNode import OctreeNode

from Config.Run.config import Config


class OctreeBuilder(object):

    MAX_CHILD_NODES = 8

    __slots__ = ('x0', 'x1', 'y0', 'y1', 'z0', 'z1', 'root_node', 'objects')

    def __init__(self, **kwargs):

        self.x0: float = kwargs.pop('x0')
        self.x1: float = kwargs.pop('x1')
        self.y0: float = kwargs.pop('y0')
        self.y1: float = kwargs.pop('y1')

        # FIXME: should get actual height for each map (use ADT, WDT, WMO for this purpose)
        self.z0 = -2000.0
        self.z1 = 2000.0

        self.root_node: OctreeNode = OctreeNode(x0=self.x0, x1=self.x1, y0=self.y0, y1=self.y1, z0=self.z0, z1=self.z1)
        self.objects: Dict = kwargs.pop('objects', {})

    def build(self) -> OctreeNode:
        self._build_child_nodes(self.root_node)

        for obj in self.objects.values():
            OctreeBuilder.set_object(self.root_node, obj)

        return self.root_node

    def _build_child_nodes(self, node: OctreeNode) -> None:
        middle_x = (node.x0 + node.x1) / 2
        middle_y = (node.y0 + node.y1) / 2
        middle_z = (node.z0 + node.z1) / 2

        x = ((node.x0, middle_x), (middle_x, node.x1))
        y = ((node.y0, middle_y), (middle_y, node.y1))
        z = ((node.z0, middle_z), (middle_z, node.z1))

        child_nodes: List[OctreeNode] = []

        for i in range(1, OctreeBuilder.MAX_CHILD_NODES + 1):
            x0, x1 = x[i % 2 == 0]
            y0, y1 = y[(i & 3) % 3 == 0]
            z0, z1 = z[i > 4]

            child_node: OctreeNode = OctreeBuilder._build_node(
                x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1, parent_node=node
            )

            if OctreeBuilder.can_contain_child_nodes(child_node):
                self._build_child_nodes(child_node)
            else:
                child_node.guids = []

            child_nodes.append(child_node)

        node.child_nodes = child_nodes

    @staticmethod
    def set_object(node: OctreeNode, obj: Union[Unit, Player]) -> None:
        if node.child_nodes:
            child_node = OctreeBuilder._get_nearest_child_node(node, obj)
            OctreeBuilder.set_object(child_node, obj)
        else:
            node.guids.append(obj.guid)

    @staticmethod
    def should_contain_object(node: OctreeNode, obj: Union[Unit, Player]) -> bool:
        return (node.x0 <= obj.x <= node.x1 and
                node.y0 <= obj.y <= node.y1 and
                node.z0 <= obj.z <= node.z1)

    @staticmethod
    def _get_nearest_child_node(node: OctreeNode, obj: Union[Unit, Player]) -> Union[OctreeNode, None]:
        for i in range(0, OctreeBuilder.MAX_CHILD_NODES):
            if OctreeBuilder.should_contain_object(node.child_nodes[i], obj):
                return node.child_nodes[i]

        return None

    @staticmethod
    def can_contain_child_nodes(node: OctreeNode) -> bool:
        update_dist = Config.World.Gameplay.update_dist

        return ((node.x1 - node.x0) > update_dist and
                (node.y1 - node.y0) > update_dist and
                (node.z1 - node.z0) > update_dist)

    @staticmethod
    def _build_node(**kwargs) -> OctreeNode:
        x0: float = kwargs.pop('x0')
        x1: float = kwargs.pop('x1')
        y0: float = kwargs.pop('y0')
        y1: float = kwargs.pop('y1')
        z0: float = kwargs.pop('z0')
        z1: float = kwargs.pop('z1')

        parent_node: OctreeNode = kwargs.pop('parent_node')

        return OctreeNode(x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1, parent_node=parent_node)
