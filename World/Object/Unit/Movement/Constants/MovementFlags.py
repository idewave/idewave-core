from enum import Enum


class MovementFlags(Enum):

    NONE               = 0x00000000
    FORWARD            = 0x00000001
    BACKWARD           = 0x00000002
    STRAFE_LEFT        = 0x00000004
    STRAFE_RIGHT       = 0x00000008
    TURN_LEFT          = 0x00000010
    TURN_RIGHT         = 0x00000020
    PITCH_UP           = 0x00000040
    PITCH_DOWN         = 0x00000080
    WALK_MODE          = 0x00000100        # Walking
    ONTRANSPORT        = 0x00000200        # Used for flying on some creatures
    LEVITATING         = 0x00000400
    ROOT               = 0x00000800
    FALLING            = 0x00001000
    FALLINGFAR         = 0x00004000
    SWIMMING           = 0x00200000        # appears with fly flag also
    ASCENDING          = 0x00400000        # swim up also
    CAN_FLY            = 0x00800000
    FLYING             = 0x01000000
    FLYING2            = 0x02000000        # Actual flying mode
    SPLINE_ELEVATION   = 0x04000000        # used for flight paths
    SPLINE_ENABLED     = 0x08000000        # used for flight paths
    WATERWALKING       = 0x10000000        # prevent unit from falling through water
    SAFE_FALL          = 0x20000000        # active rogue safe fall spell (passive)
    HOVER              = 0x40000000

    @staticmethod
    def has_value(value):
        return any(value == item.value for item in MovementFlags)
