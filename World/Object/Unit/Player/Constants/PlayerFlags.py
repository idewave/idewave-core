from enum import Enum


class PlayerFlags(Enum):

    NONE                   = 0x00000000
    GROUP_LEADER           = 0x00000001
    AFK                    = 0x00000002
    DND                    = 0x00000004
    GM                     = 0x00000008
    GHOST                  = 0x00000010
    RESTING                = 0x00000020
    UNK7                   = 0x00000040     # admin?
    FFA_PVP                = 0x00000080
    CONTESTED_PVP          = 0x00000100     # Player has been involved in a PvP combat and
                                            # will be attacked by contested guards
    PVP_DESIRED            = 0x00000200     # Stores player's permanent PvP flag preference
    HIDE_HELM              = 0x00000400
    HIDE_CLOAK             = 0x00000800
    PARTIAL_PLAY_TIME      = 0x00001000     # played long time
    NO_PLAY_TIME           = 0x00002000     # played too long time
    UNK15                  = 0x00004000
    UNK16                  = 0x00008000     # strange visual effect (2.0.1), looks like GHOST flag
    SANCTUARY              = 0x00010000     # player entered sanctuary
    TAXI_BENCHMARK         = 0x00020000     # taxi benchmark mode (on/off) (2.0.1)
    PVP_TIMER              = 0x00040000     # 3.0.2, pvp timer active (after you disable pvp manually)
    COMMENTATOR            = 0x00080000     # first appeared in TBC
