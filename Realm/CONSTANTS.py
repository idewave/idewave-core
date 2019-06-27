from enum import Enum


class RealmType(Enum):

    'In some sources also known as icon'

    NORMAL = 0
    PVP    = 1
    RP     = 6
    RPPVP  = 8


class RealmPopulation(Enum):

    LOW     = 0.5
    AVERAGE = 1.0
    HIGH    = 2.0
    FULL    = 3.0


class RealmFlags(Enum):

    NORMAL      = 0
    LOCKED      = 1  # not shown in realm list
    OFFLINE     = 2
    NEW_PLAYERS = 32
    RECOMMENDED = 64


class RealmTimezone(Enum):

    DEVELOPMENT   = 1
    UNITED_STATES = 2
    OCEANIC       = 3
    LATIN_AMERICA = 4
    TOURNAMENT    = 5
    RUSSIAN       = 12
    TAIWAN        = 14
    CHINA         = 16
    TEST_SERVER   = 26
    QA_SERVER     = 28