from typing import Union, List


class OctreeNode(object):

    __slots__ = (
        'x0',
        'x1',
        'y0',
        'y1',
        'z0',
        'z1',
        'parent_node',
        'child_nodes',
        'guids'
    )

    def __init__(self, **kwargs):
        self.x0: float = kwargs.pop('x0')
        self.x1: float = kwargs.pop('x1')
        self.y0: float = kwargs.pop('y0')
        self.y1: float = kwargs.pop('y1')
        self.z0: float = kwargs.pop('z0')
        self.z1: float = kwargs.pop('z1')

        self.parent_node: Union[OctreeNode, None] = kwargs.pop('parent_node', None)
        self.child_nodes: Union[List, None] = None

        self.guids: Union[List[int], None] = None
