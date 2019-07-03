from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import orm

from DB.BaseModel import BaseModel
from World.Object.model import Object
from World.Object.Constants.ObjectType import ObjectType
from World.Object.Constants.HighGuid import HighGuid
from World.Object.Constants.TypeMask import TypeMask
from World.Object.Position import Position
from Utils.Debug.Logger import Logger

from Config.Run.config import Config


class UnitTemplate(BaseModel):

    __tablename__ = 'unit_template'

    id                          = BaseModel.column(type='integer', primary_key=True)
    entry                       = BaseModel.column(type='integer', unique=True)
    name                        = BaseModel.column(type='string')
    sub_name                    = BaseModel.column(type='string')
    min_level                   = BaseModel.column(type='integer')
    max_level                   = BaseModel.column(type='integer')
    display_id_1                = BaseModel.column(type='integer')
    display_id_2                = BaseModel.column(type='integer')
    display_id_3                = BaseModel.column(type='integer')
    display_id_4                = BaseModel.column(type='integer')
    faction_template            = BaseModel.column(type='integer')
    scale_x                     = BaseModel.column(type='float', default=1.0)
    family                      = BaseModel.column(type='integer')
    creature_type               = BaseModel.column(type='integer')
    inhabit_type                = BaseModel.column(type='integer')
    regenerate_stats            = BaseModel.column(type='integer')
    is_racial_leader            = BaseModel.column(type='tinyint')
    npc_flags                   = BaseModel.column(type='integer')
    unit_flags                  = BaseModel.column(type='integer')
    dynamic_flags               = BaseModel.column(type='integer')
    extra_flags                 = BaseModel.column(type='integer')
    creature_type_flags         = BaseModel.column(type='integer')
    speed_walk                  = BaseModel.column(type='float')
    speed_run                   = BaseModel.column(type='float')
    unit_class                  = BaseModel.column(type='tinyint')
    rank                        = BaseModel.column(type='integer')
    health_multiplier           = BaseModel.column(type='float')
    power_multiplier            = BaseModel.column(type='float')
    damage_multiplier           = BaseModel.column(type='float')
    damage_variance             = BaseModel.column(type='float')
    armor_multiplier            = BaseModel.column(type='float')
    experience_multiplier       = BaseModel.column(type='float')
    min_health                  = BaseModel.column(type='integer')
    max_health                  = BaseModel.column(type='integer')
    min_mana                    = BaseModel.column(type='integer')
    max_mana                    = BaseModel.column(type='integer')
    min_damage                  = BaseModel.column(type='integer')
    max_damage                  = BaseModel.column(type='integer')
    min_ranged_damage           = BaseModel.column(type='float')
    max_ranged_damage           = BaseModel.column(type='float')
    armor                       = BaseModel.column(type='integer')
    melee_attack_power          = BaseModel.column(type='integer')
    ranged_attack_power         = BaseModel.column(type='integer')
    melee_base_attack_time      = BaseModel.column(type='integer')
    ranged_base_attack_time     = BaseModel.column(type='integer')
    damage_school               = BaseModel.column(type='tinyint')
    min_loot_gold               = BaseModel.column(type='integer')
    max_loot_gold               = BaseModel.column(type='integer')
    mechanic_immune_mask        = BaseModel.column(type='integer')
    resistance_holy             = BaseModel.column(type='integer')
    resistance_fire             = BaseModel.column(type='integer')
    resistance_nature           = BaseModel.column(type='integer')
    resistance_frost            = BaseModel.column(type='integer')
    resistance_shadow           = BaseModel.column(type='integer')
    resistance_arcane           = BaseModel.column(type='integer')
    movement_type               = BaseModel.column(type='tinyint')
    trainer_type                = BaseModel.column(type='tinyint')
    trainer_spell               = BaseModel.column(type='integer')
    trainer_class               = BaseModel.column(type='tinyint')
    trainer_race                = BaseModel.column(type='tinyint')
    is_civilian                 = BaseModel.column(type='tinyint')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }


class Unit(Object):

    id                      = Object.column(type='integer',
                                            foreign_key=Config.Database.DBNames.realm_db + '.object.id',
                                            primary_key=True)
    health                  = Object.column(type='integer')
    max_health              = Object.column(type='integer')
    mana                    = Object.column(type='integer')
    max_mana                = Object.column(type='integer')
    rage                    = Object.column(type='integer')
    max_rage                = Object.column(type='integer')
    focus                   = Object.column(type='integer')
    max_focus               = Object.column(type='integer')
    energy                  = Object.column(type='integer')
    max_energy              = Object.column(type='integer')
    happiness               = Object.column(type='integer')
    max_happiness           = Object.column(type='integer')
    race                    = Object.column(type='integer')
    char_class              = Object.column(type='integer')
    gender                  = Object.column(type='integer')
    level                   = Object.column(type='integer', length=3)
    unit_flags              = Object.column(type='integer')
    display_id              = Object.column(type='integer')
    native_display_id       = Object.column(type='integer')
    faction_template        = Object.column(type='integer')
    min_damage              = Object.column(type='integer')
    max_damage              = Object.column(type='integer')
    min_offhand_damage      = Object.column(type='integer')
    max_offhand_damage      = Object.column(type='integer')
    unit_bytes_1            = Object.column(type='integer')
    mod_cast_speed          = Object.column(type='float')
    strength                = Object.column(type='integer')
    agility                 = Object.column(type='integer')
    stamina                 = Object.column(type='integer')
    intellect               = Object.column(type='integer')
    spirit                  = Object.column(type='integer')
    resistance_fire         = Object.column(type='integer')
    resistance_nature       = Object.column(type='integer')
    resistance_frost        = Object.column(type='integer')
    resistance_shadow       = Object.column(type='integer')
    resistance_arcane       = Object.column(type='integer')
    armor                   = Object.column(type='integer')
    attack_power            = Object.column(type='integer')
    base_mana               = Object.column(type='integer')
    base_health             = Object.column(type='integer')
    unit_bytes_2            = Object.column(type='integer')
    ranged_attack_power     = Object.column(type='integer')
    min_ranged_damage       = Object.column(type='integer')
    max_ranged_damage       = Object.column(type='integer')
    x                       = Object.column(type='float')
    y                       = Object.column(type='float')
    z                       = Object.column(type='float')
    orientation             = Object.column(type='float')
    map_id                  = Object.column(type='integer')
    power_type              = Object.column(type='integer')

    unit_template_id        = Object.column(type='integer',
                                            foreign_key=Config.Database.DBNames.world_db + '.unit_template.id',
                                            nullable=True)

    region_id               = Object.column(type='integer',
                                            foreign_key=Config.Database.DBNames.world_db + '.region.id',
                                            nullable=True)

    unit_template           = relationship('UnitTemplate', lazy='subquery')
    region                  = relationship('Region', lazy='subquery')

    __table_args__ = {
        'schema': Config.Database.DBNames.realm_db
    }

    def __init__(self):
        self._target = None

    # this uses on session.query() etc
    @orm.reconstructor
    def init_on_load(self):
        self._target = None

    @hybrid_property
    def target(self):
        return self._target

    @target.setter
    def target(self, guid: int):
        self._target = guid

    @hybrid_property
    def object_type(self):
        return ObjectType.UNIT.value

    @hybrid_property
    def type_mask(self):
        return TypeMask.UNIT.value

    @hybrid_property
    def high_guid(self):
        return HighGuid.HIGHGUID_UNIT.value

    @hybrid_property
    def entry(self):
        if self.unit_template is not None:
            return self.unit_template.entry
        else:
            return None

    @hybrid_property
    def position(self):
        return Position(x=self.x, y=self.y, z=self.z, orientation=self.orientation)

    @position.setter
    def position(self, new_position: Position):
        self.x = new_position.x
        self.y = new_position.y
        self.z = new_position.z
        self.orientation = new_position.orientation
