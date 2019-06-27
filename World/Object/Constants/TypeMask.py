from enum import Enum


class TypeMask(Enum):

    OBJECT         = 0x0001
    ITEM           = 0x0002
    CONTAINER      = 0x0006
    UNIT           = 0x0008 | OBJECT
    PLAYER         = 0x0010 | UNIT | OBJECT
    GAMEOBJECT     = 0x0020
    DYNAMICOBJECT  = 0x0040
    CORPSE         = 0x0080
    SEER           = UNIT | DYNAMICOBJECT
