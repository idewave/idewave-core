from enum import Enum


class UnitClass(Enum):

    WARRIOR             = 1  # Has increased health and no mana
    PALADIN             = 2  # Has increased health and low mana
    ROGUE               = 4  # Has increased damage, but lower armor
    MAGE                = 8  # Has low health, but increased mana
