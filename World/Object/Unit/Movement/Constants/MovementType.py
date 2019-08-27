from enum import Enum


class MovementType(Enum):

    IDLE_ON_SPANW_POINT         = 0
    RANDOM_MOVEMENT             = 1  # should set spawndistance radius
    WAYPOINT_MOVEMENT           = 2