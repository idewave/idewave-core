from enum import Enum


class Language(Enum):
    
    UNIVERSAL       = 0
    ORCISH          = 1
    DARNASSIAN      = 2
    TAURAHE         = 3
    DWARVISH        = 6
    COMMON          = 7
    DEMONIC         = 8
    TITAN           = 9
    THALASSIAN      = 10
    DRACONIC        = 11
    KALIMAG         = 12
    GNOMISH         = 13
    TROLL           = 14
    GUTTERSPEAK     = 33
    DRAENEI         = 35
    ZOMBIE          = 36
    GNOMISH_BINARY  = 37
    GOBLIN_BINARY   = 38
    ADDON           = 0xFFFFFFFF


class LanguageSkill(Enum):

    COMMON              = 98
    ORCISH              = 109
    DWARVEN             = 111
    DARNASSIAN          = 113
    TAURAHE             = 115
    THALASSIAN          = 137
    DRACONIC            = 138
    DEMON_TONGUE        = 139
    TITAN               = 140
    OLD_TONGUE          = 141
    GNOMISH             = 313
    TROLL               = 315
    GUTTERSPEAK         = 673
    DRAENEI             = 759
