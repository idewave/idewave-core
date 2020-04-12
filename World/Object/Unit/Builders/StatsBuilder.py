from random import randrange
from types import SimpleNamespace
from typing import Union

from World.Object.Unit.Player.Constants.CharacterRace import CharacterRace
from World.Object.Unit.Player.Constants.CharacterClass import CharacterClass
from World.Object.Unit.Player.Constants.CharacterBaseStats import BASE_STATS, BASE_STATS_MOD
from World.Object.Unit.Player.Constants.AttributesPerLevel import ATTRIBUTES_PER_LEVEL
from World.Object.Unit.Constants.UnitFlags import UnitFlags
from World.Object.Unit.model import Unit, UnitTemplate
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Constants.UnitPower import UnitPower
from Typings.Abstract.AbstractBuilder import AbstractBuilder


class StatsStorage(SimpleNamespace):

    def __getattr__(self, item):
        # if stat not exists return 0 by default
        return 0

    def __iter__(self):
        yield from self.__dict__


class StatsBuilder(AbstractBuilder):

    BASE_STAMINA_LIMIT = 20

    def __init__(self, source: Union[Unit, UnitTemplate, Player]):
        self.source = source
        self.stats = StatsStorage()

    def build(self):
        if isinstance(self.source, Player):
            self._build_stats_for_player()
        elif isinstance(self.source, UnitTemplate):
            self._build_stats_from_unit_template()
        elif isinstance(self.source, Unit):
            self._build_stats_for_unit()

        self._build_stats_for_both()

        return self

    def get_stats(self):
        return self.stats

    def _build_stats_for_player(self):
        player = self.source

        self.stats.agility = StatsBuilder._get_agility(player)
        self.stats.intellect = StatsBuilder._get_intellect(player)
        self.stats.strength = StatsBuilder._get_strength(player)
        self.stats.stamina = StatsBuilder._get_stamina(player)
        self.stats.spirit = StatsBuilder._get_spirit(player)

        self.stats.power_type = StatsBuilder._set_power_type(player)
        self._set_power_depend_on_type()

        self.stats.level = player.level

        self.stats.money = StatsBuilder.from_config('player:default:start_money')
        self.stats.block = self._get_block()
        self.stats.parry = self._get_parry()

        self.stats.base_mana = StatsBuilder._get_base_mana(player)
        # TODO: should look into formula
        mana = self.get_mana(player)
        self.stats.mana = self.stats.max_mana = mana

    def _build_stats_from_unit_template(self):
        unit_template = self.source

        self.stats.level = randrange(unit_template.min_level, unit_template.max_level + 1)

    def _build_stats_for_unit(self):
        unit = self.source

        self.stats.unit_flags = UnitFlags.UNK_0.value
        self.stats.level = self.source.level

    def _build_stats_for_both(self):
        source = self.source

        self.stats.resistance_fire = source.resistance_fire
        self.stats.resistance_nature = source.resistance_nature
        self.stats.resistance_frost = source.resistance_frost
        self.stats.resistance_shadow = source.resistance_shadow
        self.stats.resistance_arcane = source.resistance_arcane

        self.stats.armor = self._get_armor()
        # TODO: should look into formulas
        self.stats.health = self.stats.base_health = self.stats.max_health = self._get_health()

    def _get_armor(self):
        armor = 0
        if isinstance(self.source, Player):
            # Players gets armor only from items, potions, spells and auras
            pass
        elif isinstance(self.source, UnitTemplate):
            armor += self.source.armor
        return armor

    def _get_health(self):
        health = 0
        if isinstance(self.source, Player):
            current_stamina = StatsBuilder._get_stamina(self.source)
            base_stamina = current_stamina if current_stamina < 20 else self.BASE_STAMINA_LIMIT
            more_stamina = current_stamina - base_stamina
            health += (base_stamina + (more_stamina * 10))
        elif isinstance(self.source, UnitTemplate):
            health += randrange(self.source.min_health, self.source.min_health + 1)
        elif isinstance(self.source, Unit):
            health += self.source.health

        return health

    def _get_block(self):
        # TODO: need check if has shield
        block = StatsBuilder.from_config('unit:default:base_block')
        return block

    def _get_parry(self):
        # TODO: need check if has weapon
        parry = StatsBuilder.from_config('unit:default:base_parry')
        return parry

    @staticmethod
    def _get_agility(player: Player):
        base_stat = StatsBuilder._get_base_attribute('agility', player)
        return base_stat

    @staticmethod
    def _get_intellect(player: Player):
        base_stat = StatsBuilder._get_base_attribute('intellect', player)
        return base_stat

    @staticmethod
    def _get_strength(player: Player):
        base_stat = StatsBuilder._get_base_attribute('strength', player)
        return base_stat

    @staticmethod
    def _get_stamina(player: Player):
        base_stat = StatsBuilder._get_base_attribute('stamina', player)
        return base_stat

    @staticmethod
    def _get_spirit(player: Player):
        base_stat = StatsBuilder._get_base_attribute('spirit', player)
        return base_stat

    @staticmethod
    def _get_base_attribute(attribute, player: Player):
        race = CharacterRace(player.race)
        char_class = CharacterClass(player.char_class)
        mod = BASE_STATS_MOD[race][attribute]
        base_stat = BASE_STATS[char_class][attribute]
        return base_stat[player.level] - abs(mod * player.level)

    @staticmethod
    def _get_base_mana(player: Player):
        char_class = CharacterClass(player.char_class)
        base_stats = BASE_STATS[char_class]
        if 'base_mana' in base_stats:
            base_stat = base_stats['base_mana']
            return base_stat[player.level]
        else:
            return 0

    def get_mana(self, player: Player):
        mana_total = self.stats.base_mana

        char_class = CharacterClass(player.char_class)
        modifiers = ATTRIBUTES_PER_LEVEL[char_class]
        modifier_intellect = modifiers.get("intellect", None)
        if modifier_intellect:
            modifier_mana = modifier_intellect.get("mana", None)
            mana_total += self.stats.intellect * modifier_mana

        return mana_total

    @staticmethod
    def _set_power_type(player: Player):
        mana_classes = [
            CharacterClass.HUNTER,
            CharacterClass.WARLOCK,
            CharacterClass.SHAMAN,
            CharacterClass.MAGE,
            CharacterClass.PRIEST,
            CharacterClass.DRUID,
            CharacterClass.PALADIN
        ]

        rage_classes = [
            CharacterClass.WARRIOR
        ]

        energy_classes = [
            CharacterClass.ROGUE
        ]

        char_class = CharacterClass(player.char_class)

        if char_class in mana_classes:
            return UnitPower.MANA.value

        elif char_class in rage_classes:
            return UnitPower.RAGE.value

        elif char_class in energy_classes:
            return UnitPower.ENERGY.value

        else:
            return UnitPower.MANA.value

    def _set_power_depend_on_type(self):
        if self.stats.power_type == UnitPower.MANA.value:
            self.stats.mana = 0
            self.stats.max_mana = 0
        elif self.stats.power_type == UnitPower.RAGE.value:
            self.stats.rage = 0
            self.stats.max_rage = 0
        elif self.stats.power_type == UnitPower.ENERGY.value:
            self.stats.energy = 0
            self.stats.max_energy = 0
