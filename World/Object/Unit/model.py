from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import orm, Column, Integer, Float, ForeignKey, String, SmallInteger

from DB.BaseModel import WorldModel
from World.Object.model import ObjectWithPosition
from World.Object.Constants import (
    ObjectType,
    HighGuid,
    TypeMask
)
from World.Object.Position import Position
from World.Region.model import Region


class UnitTemplate(WorldModel):

    id = Column(Integer, primary_key=True)
    entry = Column(Integer, unique=True)
    name = Column(String(128))
    sub_name = Column(String(128))
    min_level = Column(Integer)
    max_level = Column(Integer)
    display_id_1 = Column(Integer)
    display_id_2 = Column(Integer)
    display_id_3 = Column(Integer)
    display_id_4 = Column(Integer)
    faction_template = Column(Integer)

    @declared_attr
    def scale_x(self):
        return Column(Float, default=self.from_config("object:default:scale_x"))

    family = Column(Integer)
    creature_type = Column(Integer)
    inhabit_type = Column(Integer)
    regenerate_stats = Column(Integer)
    is_racial_leader = Column(SmallInteger)
    npc_flags = Column(Integer)
    unit_flags = Column(Integer)
    dynamic_flags = Column(Integer)
    extra_flags = Column(Integer)
    creature_type_flags = Column(Integer)
    speed_walk = Column(Float)
    speed_run = Column(Float)
    unit_class = Column(SmallInteger)
    rank = Column(Integer)
    health_multiplier = Column(Float)
    power_multiplier = Column(Float)
    damage_multiplier = Column(Float)
    damage_variance = Column(Float)
    armor_multiplier = Column(Float)
    experience_multiplier = Column(Float)
    min_health = Column(Integer)
    max_health = Column(Integer)
    min_mana = Column(Integer)
    max_mana = Column(Integer)
    min_damage = Column(Integer)
    max_damage = Column(Integer)
    min_ranged_damage = Column(Float)
    max_ranged_damage = Column(Float)
    armor = Column(Integer)
    melee_attack_power = Column(Integer)
    ranged_attack_power = Column(Integer)
    melee_base_attack_time = Column(Integer)
    ranged_base_attack_time = Column(Integer)
    damage_school = Column(SmallInteger)
    min_loot_gold = Column(Integer)
    max_loot_gold = Column(Integer)
    mechanic_immune_mask = Column(Integer)
    resistance_holy = Column(Integer)
    resistance_fire = Column(Integer)
    resistance_nature = Column(Integer)
    resistance_frost = Column(Integer)
    resistance_shadow = Column(Integer)
    resistance_arcane = Column(Integer)
    movement_type = Column(SmallInteger)
    trainer_type = Column(SmallInteger)
    trainer_spell = Column(Integer)
    trainer_class = Column(SmallInteger)
    trainer_race = Column(SmallInteger)
    is_civilian = Column(SmallInteger)


class AbstractUnit(ObjectWithPosition):

    __abstract__ = True

    level = Column(Integer)
    health = Column(Integer)
    max_health = Column(Integer)
    mana = Column(Integer)
    max_mana = Column(Integer)
    resistance_fire = Column(Integer)
    resistance_nature = Column(Integer)
    resistance_frost = Column(Integer)
    resistance_shadow = Column(Integer)
    resistance_arcane = Column(Integer)
    armor = Column(Integer)
    base_mana = Column(Integer)
    base_health = Column(Integer)
    power_type = Column(Integer)
    attack_power = Column(Integer)
    ranged_attack_power = Column(Integer)
    faction_template = Column(Integer)
    unit_bytes_1 = Column(Integer)
    unit_bytes_2 = Column(Integer)

    @declared_attr
    def region_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:world_db")}.{Region.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            ),
            nullable=True
        )

    @declared_attr
    def region(self):
        return relationship('Region', lazy='subquery')


class Unit(AbstractUnit):

    unit_id = Column('id', Integer, primary_key=True)
    native_display_id = Column(Integer)
    min_damage = Column(Integer)
    max_damage = Column(Integer)
    min_offhand_damage = Column(Integer)
    max_offhand_damage = Column(Integer)
    min_ranged_damage = Column(Integer)
    max_ranged_damage = Column(Integer)
    mod_cast_speed = Column(Float)
    unit_flags = Column(Integer)

    @declared_attr
    def unit_template_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:world_db")}.{UnitTemplate.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            ),
            nullable=True
        )

    unit_template = relationship('UnitTemplate', lazy='subquery')

    def __init__(self):
        super().__init__()
        self._target = None

    # this uses on session.query() etc
    @orm.reconstructor
    def init_on_load(self):
        # super().init_on_load()
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
    def position(self):
        return Position(x=self.x, y=self.y, z=self.z, orientation=self.orientation)

    @position.setter
    def position(self, new_position: Position):
        self.x = new_position.x
        self.y = new_position.y
        self.z = new_position.z
        self.orientation = new_position.orientation
