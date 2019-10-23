from typing import Union

from World.Object.Unit.model import Unit
from World.Object.Unit.Player.model import Player

from World.Region.Octree.OctreeNode import OctreeNode
from World.Region.Octree.Constants.OctreeConfig import MAX_CHILD_NODES


class OctreeNodeManager(object):

    @staticmethod
    def set_object(node: OctreeNode, obj: Union[Unit, Player]) -> None:
        if node.child_nodes:
            child_node = OctreeNodeManager._get_nearest_child_node(node, obj)
            OctreeNodeManager.set_object(child_node, obj)
        else:
            node.guids.append(obj.guid)
            obj.set_current_node(node)

    @staticmethod
    def _get_nearest_child_node(node: OctreeNode, obj: Union[Unit, Player]) -> Union[OctreeNode, None]:
        for i in range(0, MAX_CHILD_NODES):
            if OctreeNodeManager.should_contain_object(node.child_nodes[i], obj):
                return node.child_nodes[i]

        return None

    @staticmethod
    def should_contain_object(node: OctreeNode, obj: Union[Unit, Player]) -> bool:
        return (node.x0 <= obj.x <= node.x1 and
                node.y0 <= obj.y <= node.y1 and
                node.z0 <= obj.z <= node.z1)
