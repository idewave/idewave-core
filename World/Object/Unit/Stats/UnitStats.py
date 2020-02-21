class UnitStats(object):

    def __init__(self):
        # POWERS
        self.health: int = 0
        self.max_health: int = 0
        self.base_health: int = 0

        self.mana: int = 0              # POWER1 aka POWER_MANA
        self.max_mana: int = 0
        self.base_mana: int = 0

        self.rage: int = 0              # POWER2 aka POWER_RAGE
        self.max_rage: int = 0

        self.focus: int = 0             # POWER3 aka POWER_FOCUS
        self.max_focus: int = 0

        self.energy: int = 0            # POWER4 aka POWER_ENERGY
        self.max_energy: int = 0

        self.happiness: int = 0         # POWER5 aka POWER_HAPPINESS
        self.max_happiness: int = 0

        # BASE STATS
        self.strength: int = 0
        self.agility: int = 0
        self.stamina: int = 0
        self.intellect: int = 0
        self.spirit: int = 0

        # RESISTANCES
        self.resistance_fire: int = 0
        self.resistance_nature: int = 0
        self.resistance_frost: int = 0
        self.resistance_shadow: int = 0
        self.resistance_arcane: int = 0
        self.armor: int = 0

        # ATTACK
        self.attack_power: int = 0
        self.ranged_attack_power: int = 0

        self.min_damage: int = 0
        self.max_damage: int = 0
        self.min_offhand_damage: int = 0
        self.max_offhand_damage: int = 0
        self.min_ranged_damage: int = 0
        self.max_ranged_damage: int = 0

        self.attack_time_mainhand: int = 0
        self.attack_time_offhand: int = 0

        # CAST
        self.mod_cast_speed: int = 0

    def __iter__(self):
        yield from self.__dict__
