from typing import List

from World.Region.Octree.Node import RootNode, ChildNode, LeafNode
from World.Region.Octree.Constants import MAX_CHILD_NODES
from Typings.Constants import NON_LEAF_NODE, CHILD_NODE
from Typings.Abstract import AbstractBuilder

from World.Region.Octree.OctreeNodeManager import OctreeNodeManager
from World.Object.model import ObjectWithPosition
from Config.Mixins import ConfigurableMixin


class OctreeBuilder(AbstractBuilder, ConfigurableMixin):

    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'root_node',
        'objects'
    )

    def __init__(self, **kwargs):

        self.x0: float = kwargs.pop('x0')
        self.x1: float = kwargs.pop('x1')
        self.y0: float = kwargs.pop('y0')
        self.y1: float = kwargs.pop('y1')

        # FIXME: should get actual height for each map (use ADT, WDT, WMO for this purpose)
        self.z0 = -2000.0
        self.z1 = 2000.0

        self.root_node: RootNode = RootNode(
            x0=self.x0,
            x1=self.x1,
            y0=self.y0,
            y1=self.y1,
            z0=self.z0,
            z1=self.z1
        )
        self.objects: List[ObjectWithPosition] = kwargs.pop('objects', [])

    def build(self) -> RootNode:
        self._build_child_nodes(self.root_node)

        # for obj in self.objects.values():
        #     OctreeBuilder.set_object(self.root_node, obj)

        for obj in self.objects:
            OctreeNodeManager.add_object(self.root_node, obj)

        return self.root_node

    def _build_child_nodes(self, node: NON_LEAF_NODE) -> None:
        middle_x = (node.x0 + node.x1) / 2
        middle_y = (node.y0 + node.y1) / 2
        middle_z = (node.z0 + node.z1) / 2

        x = ((node.x0, middle_x), (middle_x, node.x1))
        y = ((node.y0, middle_y), (middle_y, node.y1))
        z = ((node.z0, middle_z), (middle_z, node.z1))

        child_nodes: List[CHILD_NODE] = []

        for i in range(1, MAX_CHILD_NODES + 1):
            x0, x1 = x[i % 2 == 0]
            y0, y1 = y[(i & 3) % 3 == 0]
            z0, z1 = z[i > 4]

            child_node: CHILD_NODE = OctreeBuilder._build_node(
                x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1, parent_node=node
            )

            if OctreeBuilder.can_contain_child_nodes(child_node):
                self._build_child_nodes(child_node)
            else:
                child_node = OctreeBuilder._build_leaf(
                    x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1, parent_node=node
                )

            child_nodes.append(child_node)

        node.child_nodes = child_nodes

    @staticmethod
    def can_contain_child_nodes(node: ChildNode) -> bool:
        octree_node_size = OctreeBuilder.from_config('region:generation:octree_node_size')

        return ((node.x1 - node.x0) > octree_node_size and
                (node.y1 - node.y0) > octree_node_size and
                (node.z1 - node.z0) > octree_node_size)

    @staticmethod
    def _build_node(**kwargs) -> ChildNode:
        x0: float = kwargs.pop('x0')
        x1: float = kwargs.pop('x1')
        y0: float = kwargs.pop('y0')
        y1: float = kwargs.pop('y1')
        z0: float = kwargs.pop('z0')
        z1: float = kwargs.pop('z1')

        parent_node: ChildNode = kwargs.pop('parent_node')

        return ChildNode(
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            z0=z0,
            z1=z1,
            parent_node=parent_node
        )

    @staticmethod
    def _build_leaf(**kwargs) -> LeafNode:
        x0: float = kwargs.pop('x0')
        x1: float = kwargs.pop('x1')
        y0: float = kwargs.pop('y0')
        y1: float = kwargs.pop('y1')
        z0: float = kwargs.pop('z0')
        z1: float = kwargs.pop('z1')

        parent_node: ChildNode = kwargs.pop('parent_node')

        return LeafNode(
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            z0=z0,
            z1=z1,
            parent_node=parent_node
        )
