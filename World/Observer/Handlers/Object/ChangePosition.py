from typing import List

from Typings.Abstract import AbstractHandler
from World.Object.model import ObjectWithPosition
from World.Region.model import Region
from World.Region.Octree.OctreeNodeManager import OctreeNodeManager


class ChangePosition(AbstractHandler):

    __slots__ = (
        'subscribers',
        'object',
        'move_from',
        'move_to'
    )

    def __init__(self, **kwargs):
        self.subscribers: List[ObjectWithPosition] = kwargs.pop('subscribers')
        self.object: ObjectWithPosition = kwargs.pop('object')
        self.move_from: Region = kwargs.pop('move_from')
        self.move_to: Region = kwargs.pop('move_to')

    async def process(self):
        OctreeNodeManager.remove_object(root_node=self.move_from.get_octree(), obj=self.object)
        OctreeNodeManager.add_object(root_node=self.move_to.get_octree(), obj=self.object)
