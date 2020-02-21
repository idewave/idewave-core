from World.Object.Unit.Stats.Builders.UnitStatsBuilder import UnitStatsBuilder
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Player.Constants.AttributesPerLevel import ATTRIBUTES_PER_LEVEL
from World.Object.Unit.Player.Stats.PlayerStats import PlayerStats
from World.Object.Unit.Player.Constants.CharacterBaseStats import BASE_STATS, BASE_STATS_MOD
from World.Object.Unit.Player.Constants.ExperiencePerLevel import EXP_PER_LEVEL


class PlayerStatsBuilder(UnitStatsBuilder):

    __slots__ = ('world_object', 'stats')

    def __init__(self, **kwargs):
        super(PlayerStatsBuilder, self).__init__(**kwargs)
        self.stats = PlayerStats()
        self.world_object: Player = kwargs.pop('world_object')

    def build(self):
        super().build()
        self._set_base_stats()
        self._calculate_health()
        self._calculate_mana()
        self._calculate_next_level_xp()

        return self

    def get_stats(self):
        return self.stats

    def _set_base_stats(self):
        self.stats.strength = self._get_base_stat('strength')
        self.stats.agility = self._get_base_stat('agility')
        self.stats.stamina = self._get_base_stat('stamina')
        self.stats.intellect = self._get_base_stat('intellect')
        self.stats.spirit = self._get_base_stat('spirit')

    def _calculate_health(self):
        try:
            health_per_stamina = ATTRIBUTES_PER_LEVEL[self.world_object.char_class]['stamina']['health']
            health = self.stats.base_health + self.stats.stamina * health_per_stamina
            self.stats.health = self.stats.max_health = health
        except KeyError:
            self.stats.health = self.stats.base_health

    def _calculate_mana(self):
        mana_total = self.stats.base_mana

        modifiers = ATTRIBUTES_PER_LEVEL[self.world_object.char_class]
        modifier_intellect = modifiers.get('intellect', None)
        if modifier_intellect:
            modifier_mana = modifier_intellect.get('mana', None)
            mana_total += self.stats.intellect * modifier_mana

        self.stats.mana = self.stats.max_mana = mana_total

    def _get_base_stat(self, stat: str) -> int:
        player = self.world_object
        mod = BASE_STATS_MOD[player.race][stat]
        base_stat = BASE_STATS[player.char_class][stat]
        return base_stat[player.level] - abs(mod * player.level)

    def _calculate_next_level_xp(self) -> None:
        level = self.world_object.level
        self.stats.next_level_xp = EXP_PER_LEVEL[level - 1]
