from World.Region.Octree.OctreeNode import OctreeNode

class OctreeBuilder(object):

    __slots__ = ('x0', 'x1', 'y0', 'y1', 'z0', 'z1', 'root_node', 'objects')

    def __init__(self, **kwargs):

        self.x0 = kwargs.pop('x0')
        self.x1 = kwargs.pop('x1')
        self.y0 = kwargs.pop('y0')
        self.y1 = kwargs.pop('y1')

        # FIXME: should get actual height for each map (use ADT, WDT, WMO for this purpose)
        self.z0 = -2000
        self.z1 = 2000

        self.root_node = OctreeNode(x0=self.x0, x1=self.x1, y0=self.y0, y1=self.y1, z0=self.z0, z1=self.z1)
        self.objects = kwargs.pop('objects', {})

    def build(self) -> OctreeNode:
        self._build_child_nodes(self.root_node, self.root_node)
        self.root_node.objects = self.objects
        return self.root_node

    def _set_objects(self) -> None:
        for obj in self.objects.values():
            self.root_node.set_object(obj)

    def _build_child_nodes(self, node: OctreeNode, root_node: OctreeNode) -> None:
        middle_x = (node.x0 + node.x1) / 2
        middle_y = (node.y0 + node.y1) / 2
        middle_z = (node.z0 + node.z1) / 2

        x = ((node.x0, middle_x), (middle_x, node.x1))
        y = ((node.y0, middle_y), (middle_y, node.y1))
        z = ((node.z0, middle_z), (middle_z, node.z1))

        child_nodes = []

        for i in range(1, OctreeNode.MAX_CHILD_NODES + 1):
            x0, x1 = x[i % 2 == 0]
            y0, y1 = y[(i & 3) % 3 == 0]
            z0, z1 = z[i > 4]

            child_node = OctreeBuilder._build_node(x0, x1, y0, y1, z0, z1)
            child_node.set_root_node(root_node)
            child_node.set_parent_node(node)

            if child_node.can_contain_child_nodes():
                self._build_child_nodes(child_node, root_node)
            else:
                child_node.guids = []

            child_nodes.append(child_node)

        node.set_child_nodes(child_nodes)

    @staticmethod
    def _build_node(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> OctreeNode:
        return OctreeNode(x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1)
