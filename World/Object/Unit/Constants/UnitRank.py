from enum import Enum


class UnitRank(Enum):

    NORMAL          = 0  # Default type
    ELITE           = 1  # Increased health, damage, better loot
    RARE_ELITE      = 2  # Like Elite but with increased respawn time
    WORLD_BOSS      = 3  # Highest rank, best loot, highest respawn time
    RARE_ELITE      = 4  # Increased respawn time, better loot
