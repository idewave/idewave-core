from enum import Enum


class ObjectUpdateType(Enum):

    VALUES                   = 0
    MOVEMENT                 = 1
    CREATE_OBJECT            = 2    # for entities without position: item, bag etc
    CREATE_OBJECT2           = 3    # for entities with position in space: gameobjects, corpses, creatures, players etc
    OUT_OF_RANGE_OBJECTS     = 4
    NEAR_OBJECTS             = 5


class ObjectUpdateFlags(Enum):

    UPDATEFLAG_NONE                     = 0x0000
    UPDATEFLAG_SELF                     = 0x0001
    UPDATEFLAG_TRANSPORT                = 0x0002
    UPDATEFLAG_HAS_ATTACKING_TARGET     = 0x0004
    UPDATEFLAG_LOWGUID                  = 0x0008
    UPDATEFLAG_HIGHGUID                 = 0x0010
    UPDATEFLAG_LIVING                   = 0x0020
    UPDATEFLAG_HAS_POSITION             = 0x0040
