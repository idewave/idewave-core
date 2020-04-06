from typing import List, Optional, Union


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


class RootNode(Node):
    __slots__ = (
        'child_nodes',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.child_nodes: List[Union[ChildNode, LeafNode]] = []


class ChildNode(RootNode):
    pass


class LeafNode(Node):
    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'parent_node',
        'guids'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guids = []


# class ParentNode(object):
#     __slots__ = (
#         'child_nodes',
#     )
#
#     def __init__(self):
#         self.child_nodes: List[ChildNode] = []
#
#
# class ChildNode(object):
#     __slots__ = (
#         'parent_node',
#     )
#
#     def __init__(self, **kwargs):
#         self.parent_node: ParentNode = kwargs.pop('parent_node')


# class RootNode(Node, ParentNode):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#
# class NonLeafChildNode(Node, ParentNode, ChildNode):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#
# class LeafChildNode(Node, ChildNode):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)


# class RootNode(Node):
#     __slots__ = (
#         'child_nodes',
#     )
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.x0: float = kwargs.pop('x0')
#         self.x1: float = kwargs.pop('x1')
#         self.y0: float = kwargs.pop('y0')
#         self.y1: float = kwargs.pop('y1')
#         self.z0: float = kwargs.pop('z0')
#         self.z1: float = kwargs.pop('z1')
#         self.child_nodes: List[CHILD_NODE] = []
#
#
# class ChildNode(RootNode):
#
#     __slots__ = (
#         'parent_node',
#     )
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.parent_node = kwargs.pop('parent_node')
#         self.child_nodes: List[CHILD_NODE] = []
#
#
# class LeafNode(ChildNode):
#
#     __slots__ = (
#         'guids'
#     )
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.guids: List[int] = []
