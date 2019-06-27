from enum import Enum


class NPCFlags(Enum):

    NONE                = 0
    GOSSIP              = 1
    QUESTGIVER          = 2
    VENDOR              = 4
    FLIGHTMASTER        = 8
    TRAINER             = 16
    SPIRITHEALER        = 32
    SPIRITGUIDE         = 64
    INNKEEPER           = 128
    BANKER              = 256
    PETITIONER          = 512
    TABARDDESIGNER      = 1024
    BATTLEMASTER        = 2048
    AUCTIONEER          = 4096
    STABLEMASTER        = 8192
    REPAIR              = 16384
    OUTDOOR_PVP         = 536870912
