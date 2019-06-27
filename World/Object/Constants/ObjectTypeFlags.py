from enum import Enum


class ObjectTypeFlags(Enum):

    OBJECT          = 1 << 0
    ITEM            = 1 << 1
    CONTAINER       = 1 << 2
    UNIT            = 1 << 3
    PLAYER          = 1 << 4
    GAME_OBJECT     = 1 << 5
    DYNAMIC_OBJECT  = 1 << 6
    CORPSE          = 1 << 7
