from World.Object.Unit.Stats.UnitStats import UnitStats


class PlayerStats(UnitStats):

    def __init__(self):
        super(PlayerStats, self).__init__()

        # EXPERIENCE
        self.xp: int = 0
        self.next_level_xp: int = 0
        self.rest_state_exp: int = 0

        # TALENTS
        self.free_talent_points: int = 0

        # PROFESSIONS
        self.free_primary_professions_points: int = 0

        # DEF STATS
        self.block: float = 0
        self.dodge: float = 0
        self.parry: float = 0

        # CRIT
        self.melee_crit: float = 0
        self.ranged_crit: float = 0

        # MISC
        self.max_level: int = 0

    def __iter__(self):
        yield from self.__dict__
