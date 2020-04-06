from typing import List, Optional, Union, Dict

from World.Object.model import ObjectWithPosition
from Typings.Constants import GUID


class Node(object):
    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'parent_node',
    )

    def __init__(self, **kwargs):
        self.x0: float = kwargs.pop('x0')
        self.x1: float = kwargs.pop('x1')
        self.y0: float = kwargs.pop('y0')
        self.y1: float = kwargs.pop('y1')
        self.z0: float = kwargs.pop('z0')
        self.z1: float = kwargs.pop('z1')
        self.parent_node: Optional[Union[RootNode, ChildNode]] = kwargs.get('parent_node')


class NodeWithChildren(Node):
    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'parent_node',
        'child_nodes',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.child_nodes: List[Union[ChildNode, LeafNode]] = []


class RootNode(NodeWithChildren):
    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'parent_node',
        'child_nodes',
        'guid_octree_map',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guid_octree_map: Dict[GUID, Node] = {}


class ChildNode(NodeWithChildren):
    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'parent_node',
        'child_nodes',
    )


class LeafNode(Node):
    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'parent_node',
        'objects'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.objects: List[ObjectWithPosition] = []
