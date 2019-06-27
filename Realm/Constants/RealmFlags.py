from enum import Enum


class RealmFlags(Enum):

    NORMAL      = 0
    LOCKED      = 1  # not shown in realm list
    OFFLINE     = 2
    NEW_PLAYERS = 32
    RECOMMENDED = 64
