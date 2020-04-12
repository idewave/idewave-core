from World.Object.ObjectManager import ObjectManager
from World.Object.Constants.UpdateObjectFields import UnitField
from World.Object.Unit.model import Unit, UnitTemplate
from World.Region.model import Region
from World.Object.Unit.Constants.UnitFlags import UnitFlags
from World.Object.Unit.Stats.Builders.UnitStatsBuilder import UnitStatsBuilder


class UnitManager(ObjectManager):

    __slots__ = ('world_object', 'stats')

    def __init__(self, **kwargs):
        super(UnitManager, self).__init__(**kwargs)
        self.world_object = Unit()
        self.stats = UnitStatsBuilder(world_object=self.world_object).build().get_stats()

    @property
    def unit(self):
        return self.world_object

    def add_unit_fields(self):

        stats = self.stats

        self.set_object_field(UnitField.HEALTH, stats.health)
        self.set_object_field(UnitField.POWER_MANA, stats.mana)
        self.set_object_field(UnitField.POWER_RAGE, stats.rage)
        self.set_object_field(UnitField.POWER_FOCUS, stats.focus)
        self.set_object_field(UnitField.POWER_ENERGY, stats.energy)
        self.set_object_field(UnitField.POWER_HAPPINESS, stats.happiness)

        self.set_object_field(UnitField.MAXHEALTH, stats.max_health)
        self.set_object_field(UnitField.MAXPOWER_MANA, stats.max_mana)
        self.set_object_field(UnitField.MAXPOWER_RAGE, stats.max_rage)
        self.set_object_field(UnitField.MAXPOWER_FOCUS, stats.max_focus)
        self.set_object_field(UnitField.MAXPOWER_ENERGY, stats.max_energy)
        self.set_object_field(UnitField.MAXPOWER_HAPPINESS, stats.max_happiness)

        self.set_object_field(UnitField.LEVEL, self.unit.level)
        self.set_object_field(UnitField.FACTIONTEMPLATE, self.unit.faction_template)
        self.set_object_field(UnitField.FLAGS, UnitFlags.PLAYER_CONTROLLED.value)

        self.set_object_field(UnitField.BASEATTACKTIME, stats.attack_time_mainhand)
        self.set_object_field(UnitField.OFFHANDATTACKTIME, stats.attack_time_offhand)

        self.set_object_field(UnitField.BOUNDINGRADIUS, UnitManager.from_config('unit:default:bounding_radius'))
        self.set_object_field(UnitField.COMBATREACH, UnitManager.from_config('unit:default:combat_reach'))

        if isinstance(self.unit, Unit):
            self.set_object_field(UnitField.DISPLAYID, self.unit.display_id)
            self.set_object_field(UnitField.NATIVEDISPLAYID, self.unit.native_display_id)
        elif isinstance(self.unit, UnitTemplate):
            # TODO: this should be checked
            self.set_object_field(UnitField.DISPLAYID, self.unit.display_id_1)
            self.set_object_field(UnitField.NATIVEDISPLAYID, self.unit.display_id_1)

        self.set_object_field(UnitField.MINDAMAGE, self.unit.min_damage)
        self.set_object_field(UnitField.MAXDAMAGE, self.unit.max_damage)
        self.set_object_field(UnitField.MINOFFHANDDAMAGE, self.unit.min_offhand_damage)
        self.set_object_field(UnitField.MAXOFFHANDDAMAGE, self.unit.max_offhand_damage)

        self.set_object_field(UnitField.BYTES_1, self.unit.unit_bytes_1)

        self.set_object_field(UnitField.MOD_CAST_SPEED, self.unit.mod_cast_speed)

        self.set_object_field(UnitField.STAT0, stats.strength)
        self.set_object_field(UnitField.STAT1, stats.agility)
        self.set_object_field(UnitField.STAT2, stats.stamina)
        self.set_object_field(UnitField.STAT3, stats.intellect)
        self.set_object_field(UnitField.STAT4, stats.spirit)

        self.set_object_field(UnitField.RESISTANCE_FIRE, stats.resistance_fire)
        self.set_object_field(UnitField.RESISTANCE_NATURE, stats.resistance_nature)
        self.set_object_field(UnitField.RESISTANCE_FROST, stats.resistance_frost)
        self.set_object_field(UnitField.RESISTANCE_SHADOW, stats.resistance_shadow)
        self.set_object_field(UnitField.RESISTANCE_ARCANE, stats.resistance_arcane)

        self.set_object_field(UnitField.RESISTANCE_NORMAL, stats.armor)

        self.set_object_field(UnitField.ATTACK_POWER, self.unit.attack_power)
        self.set_object_field(UnitField.BASE_MANA, self.unit.base_mana)
        self.set_object_field(UnitField.BASE_HEALTH, self.unit.base_health)
        self.set_object_field(UnitField.ATTACK_POWER_MODS, 0)

        self.set_object_field(UnitField.BYTES_2, self.unit.unit_bytes_2) # sheath, forms

        self.set_object_field(UnitField.RANGED_ATTACK_POWER, self.unit.ranged_attack_power)
        self.set_object_field(UnitField.RANGED_ATTACK_POWER_MODS, 0)
        self.set_object_field(UnitField.MINRANGEDDAMAGE, self.unit.min_ranged_damage)
        self.set_object_field(UnitField.MAXRANGEDDAMAGE, self.unit.max_ranged_damage)

    def delete(self, **kwargs):
        self.session.query(Unit).filter_by(**kwargs).delete()
        return self

    # overridable
    def load(self, **kwargs):
        id = kwargs.pop('id')
        self.world_object = self.session.query(Unit).filter_by(id=id).first()
        return self

    # overridable
    def new(self, **kwargs):
        entry = kwargs.pop('entry', None)
        identifier = kwargs.pop('identifier', None)
        x = kwargs.pop('x', None)
        y = kwargs.pop('y', None)
        z = kwargs.pop('z', None)

        # notice: at this step unit already created in constructor
        # also notice: here processed query to another DB (from current realm_db to external world_db)
        unit_template = self.session.query(UnitTemplate).filter_by(entry=entry).first()
        self.world_object.unit_template = unit_template

        region = self.session.query(Region).filter_by(identifier=identifier).first()
        self.world_object.region = region

        self.world_object.x = x
        self.world_object.y = y
        self.world_object.z = z

        # self.stats_builder = StatsBuilder(unit_template)
        # self.set_stats()
        self._set_stats()

        self._set_display_id()
        self._set_faction_template()

        return self

    # inheritable
    def prepare(self):
        super(UnitManager, self).prepare()
        self._init_stats()
        self.add_unit_fields()
        return self

    # def set_stats(self):
    #     stats = self.stats_builder.build().get_stats()
    #     for key in stats:
    #         setattr(self.world_object, key, getattr(stats, key))
    #     return self
    def _init_stats(self) -> None:
        self.stats = UnitStatsBuilder(world_object=self.unit).build().get_stats()

    def _set_stats(self) -> None:
        self._init_stats()
        stats = self.stats
        for key in stats:
            setattr(self.world_object, key, getattr(stats, key))

    def _set_display_id(self):
        self.unit.display_id = self.unit.native_display_id = self.unit.unit_template.display_id_1

    def _set_faction_template(self):
        self.unit.faction_template = self.unit.unit_template.faction_template
