from enum import Enum


class SpellCastFlags(Enum):

    CAST_FLAG_NONE              = 0x00000000
    CAST_FLAG_HIDDEN_COMBATLOG  = 0x00000001               
    CAST_FLAG_UNKNOWN2          = 0x00000002               
    CAST_FLAG_UNKNOWN3          = 0x00000004
    CAST_FLAG_UNKNOWN4          = 0x00000008
    CAST_FLAG_PERSISTENT_AA     = 0x00000010               
    CAST_FLAG_AMMO              = 0x00000020               
    CAST_FLAG_UNKNOWN7          = 0x00000040               
    CAST_FLAG_UNKNOWN8          = 0x00000080
    CAST_FLAG_UNKNOWN9          = 0x00000100               
    CAST_FLAG_UNKNOWN10         = 0x00000200
    CAST_FLAG_UNKNOWN11         = 0x00000400
    CAST_FLAG_PREDICTED_POWER   = 0x00000800               
    CAST_FLAG_UNKNOWN13         = 0x00001000
    CAST_FLAG_UNKNOWN14         = 0x00002000
    CAST_FLAG_UNKNOWN15         = 0x00004000
    CAST_FLAG_UNKNOWN16         = 0x00008000
