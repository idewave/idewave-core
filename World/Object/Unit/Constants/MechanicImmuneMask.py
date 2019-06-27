from enum import Enum


class MechanicImmuneMask(Enum):

    NONE                    = 0
    CHARM                   = 1
    CONFUSED                = 2
    DISARM                  = 4
    DISTRACT                = 8
    FEAR                    = 16
    FUMBLE                  = 32
    ROOT                    = 64
    PACIFY                  = 128
    SILENCE                 = 256
    SLEEP                   = 512
    SNARE                   = 1024
    STUN                    = 2056
    FREEZE                  = 4096
    KNOCKOUT                = 8192
    BLEED                   = 16384
    BANDAGE                 = 32768
    POLYMORPH               = 65536
    BANISH                  = 131072
    SHIELD                  = 262144
    SHACKLE                 = 524288
    MOUNT                   = 1048576
    PERSUADE                = 2097152
    TURN                    = 4194304
    HORROR                  = 8388608
    INVULNERABILITY         = 16777216
    INTERRUPT               = 33554432
    DAZE                    = 67108864
    DISCOVERY               = 134217728
    IMMUNE_SHIELD           = 268435456
    SAPPED                  = 536870912
