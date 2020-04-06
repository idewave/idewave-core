from typing import Union, Dict

from World.Object.model import Object
from World.Object.Unit.model import Unit
from World.Object.Unit.Player.model import Player
from World.Region.Octree.Node import RootNode, ChildNode, LeafNode
from World.Region.model import Region


# Object
ANY_OBJECT = Union[Object, Unit, Player]
CREATURE = Union[Unit, Player]

# Region
ANY_NODE = Union[RootNode, ChildNode, LeafNode]
CHILD_NODE = Union[ChildNode, LeafNode]
NON_LEAF_NODE = Union[RootNode, ChildNode]

REGIONS_MAP = Dict[int, Region]
