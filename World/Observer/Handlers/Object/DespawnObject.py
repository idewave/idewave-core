from typing import List

from Typings.Abstract.AbstractHandler import AbstractHandler
from World.Object.model import ObjectWithPosition
from World.Region.model import Region
from World.Region.Octree.OctreeNodeManager import OctreeNodeManager


class DespawnObject(AbstractHandler):

    def __init__(self, **kwargs):
        self.subscribers: List[ObjectWithPosition] = kwargs.pop('subscribers')
        self.object: ObjectWithPosition = kwargs.pop('object')
        self.region: Region = kwargs.pop('region')

    async def process(self):
        OctreeNodeManager.remove_object(root_node=self.region.get_octree(), obj=self.object)
