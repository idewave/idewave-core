from enum import Enum


class HighGuid(Enum):

    HIGHGUID_ITEM           = 0x4000    # blizz 4000
    HIGHGUID_CONTAINER      = 0x4000    # blizz 4000
    HIGHGUID_PLAYER         = 0x0000    # blizz 0000
    HIGHGUID_GAMEOBJECT     = 0xF110    # blizz F110
    HIGHGUID_TRANSPORT      = 0xF120    # blizz F120 (for GAMEOBJECT_TYPE_TRANSPORT)
    HIGHGUID_UNIT           = 0xF130    # blizz F130
    HIGHGUID_PET            = 0xF140    # blizz F140
    HIGHGUID_DYNAMICOBJECT  = 0xF100    # blizz F100
    HIGHGUID_CORPSE         = 0xF101    # blizz F100
    HIGHGUID_MO_TRANSPORT   = 0x1FC0    # blizz 1FC0 (for GAMEOBJECT_TYPE_MO_TRANSPORT)
    HIGHGUID_GROUP          = 0x1F50    # blizz 1F5x
