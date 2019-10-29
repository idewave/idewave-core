from enum import Enum


class BroadcastType(Enum):

    SAY_RANGE           = 0x01
    YELL_RANGE          = 0x02
    REGION              = 0x04
    CONTINENT           = 0x08
    WORLD               = 0x10
