from enum import Enum


class ObjectType(Enum):

    OBJECT          = 0  # 0x01 (object)
    ITEM            = 1  # 0x03 (object, item)
    CONTAINER       = 2  # 0x07 (object, item, container)
    UNIT            = 3  # 0x09 (object, unit)
    PLAYER          = 4  # 0x19 (object, unit, player)
    GAME_OBJECT     = 5  # 0x21 (object, game_object)
    DYNAMIC_OBJECT  = 6  # 0x41 (object, dynamic_object)
    CORPSE          = 7  # 0x81 (object, corpse)
