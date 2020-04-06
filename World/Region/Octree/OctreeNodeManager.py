from typing import Optional, List

from World.Region.Octree.Node import RootNode, ChildNode, LeafNode
from Typings.Constants import ANY_NODE, CHILD_NODE
from World.Object.model import ObjectWithPosition
from World.Region.Octree.Constants.Config import MAX_CHILD_NODES


class OctreeNodeManager(object):

    @staticmethod
    def get_guids(
            node: ANY_NODE,
            result: Optional[List[ObjectWithPosition]]
    ) -> List[ObjectWithPosition]:
        if result is None:
            result = []

        if node.child_nodes:
            for child in node.child_nodes:
                OctreeNodeManager.get_guids(child, result)
        else:
            result += node.objects

        return result

    @staticmethod
    def get_node(root_node: RootNode, obj: ObjectWithPosition) -> LeafNode:
        node: ANY_NODE = root_node

        while node.child_nodes:
            node: CHILD_NODE = OctreeNodeManager._get_nearest_child_node(node, obj)

        return node

    @staticmethod
    def remove_object(root_node: RootNode, obj: ObjectWithPosition) -> None:
        node: LeafNode = OctreeNodeManager.get_node(root_node, obj)
        node.objects.remove(obj)
        del root_node.guid_octree_map[obj.guid]

    @staticmethod
    def add_object(root_node: RootNode, obj: ObjectWithPosition) -> None:
        node: LeafNode = OctreeNodeManager.get_node(root_node, obj)
        node.objects.append(obj)
        root_node.guid_octree_map[obj.guid] = node

    @staticmethod
    def _get_nearest_child_node(node: ChildNode, obj: ObjectWithPosition) -> Optional[ChildNode]:
        for i in range(0, MAX_CHILD_NODES):
            if OctreeNodeManager.should_contain_object(node.child_nodes[i], obj):
                return node.child_nodes[i]

        return None

    @staticmethod
    def should_contain_object(node: ChildNode, obj: ObjectWithPosition) -> bool:
        return (node.x0 <= obj.x <= node.x1 and
                node.y0 <= obj.y <= node.y1 and
                node.z0 <= obj.z <= node.z1)

    @staticmethod
    def get_guids_in_range(
            root_node: RootNode,
            obj: ObjectWithPosition,
            distance: int
    ) -> List[ObjectWithPosition]:
        objects: List[ObjectWithPosition] = []

        node: LeafNode = OctreeNodeManager.get_node(root_node, obj)

        if node.parent_node:
            parent: ANY_NODE = node.parent_node

            if parent.parent_node:
                parent = parent.parent_node

            for node in parent.child_nodes:
                OctreeNodeManager.get_guids(node, objects)

        return objects
