from enum import Enum


class UpdateObjectFlags(Enum):

    UPDATEFLAG_NONE                     = 0x0000
    UPDATEFLAG_SELF                     = 0x0001
    UPDATEFLAG_TRANSPORT                = 0x0002
    UPDATEFLAG_HAS_ATTACKING_TARGET     = 0x0004
    UPDATEFLAG_LOWGUID                  = 0x0008
    UPDATEFLAG_HIGHGUID                 = 0x0010
    UPDATEFLAG_LIVING                   = 0x0020
    UPDATEFLAG_HAS_POSITION             = 0x0040
