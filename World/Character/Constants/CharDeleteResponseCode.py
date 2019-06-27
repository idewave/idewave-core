from enum import Enum


class CharDeleteResponseCode(Enum):

    CHAR_DELETE_IN_PROGRESS                 = 0x3A
    CHAR_DELETE_SUCCESS                     = 0x3B
    CHAR_DELETE_FAILED                      = 0x3C
    CHAR_DELETE_FAILED_LOCKED_FOR_TRANSFER  = 0x3D
    CHAR_DELETE_FAILED_GUILD_LEADER         = 0x3E
    CHAR_DELETE_FAILED_ARENA_CAPTAIN        = 0x3F
