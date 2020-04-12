from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, Float, ForeignKey, String, SmallInteger

from DB.BaseModel import WorldModel

from World.Object.model import Object
from World.Object.Constants.TypeMask import TypeMask
from World.Object.Constants.ObjectType import ObjectType
from World.Object.Constants.HighGuid import HighGuid


class ItemTemplate(WorldModel):

    id = Column(Integer, primary_key=True)
    entry = Column(Integer, unique=True)
    item_class = Column(Integer)
    item_subclass = Column(Integer)
    name = Column(String(128))
    display_id = Column(Integer)
    quality = Column(SmallInteger)
    flags = Column(Integer)
    buy_count = Column(SmallInteger)
    buy_price = Column(Integer)
    sell_price = Column(Integer)
    item_type = Column(SmallInteger)
    allowable_class = Column(Integer)
    allowable_race = Column(Integer)
    item_level = Column(SmallInteger)
    required_level = Column(SmallInteger)
    required_skill = Column(Integer)
    required_skill_rank = Column(Integer)
    required_spell = Column(Integer)
    maxcount = Column(SmallInteger)
    stackable = Column(SmallInteger)
    container_slots = Column(SmallInteger)
    stat_type1 = Column(SmallInteger)
    stat_value1 = Column(SmallInteger)
    stat_type2 = Column(SmallInteger)
    stat_value2 = Column(SmallInteger)
    stat_type3 = Column(SmallInteger)
    stat_value3 = Column(SmallInteger)
    stat_type4 = Column(SmallInteger)
    stat_value4 = Column(SmallInteger)
    stat_type5 = Column(SmallInteger)
    stat_value5 = Column(SmallInteger)
    stat_type6 = Column(SmallInteger)
    stat_value6 = Column(SmallInteger)
    stat_type7 = Column(SmallInteger)
    stat_value7 = Column(SmallInteger)
    stat_type8 = Column(SmallInteger)
    stat_value8 = Column(SmallInteger)
    stat_type9 = Column(SmallInteger)
    stat_value9 = Column(SmallInteger)
    stat_type10 = Column(SmallInteger)
    stat_value10 = Column(SmallInteger)
    dmg_min1 = Column(Float)
    dmg_max1 = Column(Float)
    dmg_type1 = Column(SmallInteger)
    dmg_min2 = Column(Float)
    dmg_max2 = Column(Float)
    dmg_type2 = Column(SmallInteger)
    dmg_min3 = Column(Float)
    dmg_max3 = Column(Float)
    dmg_type3 = Column(SmallInteger)
    dmg_min4 = Column(Float)
    dmg_max4 = Column(Float)
    dmg_type4 = Column(SmallInteger)
    dmg_min5 = Column(Float)
    dmg_max5 = Column(Float)
    dmg_type5 = Column(SmallInteger)
    armor = Column(SmallInteger)
    fire_res = Column(SmallInteger)
    nature_res = Column(SmallInteger)
    frost_res = Column(SmallInteger)
    shadow_res = Column(SmallInteger)
    arcane_res = Column(SmallInteger)
    delay = Column(SmallInteger, default=1000)
    description = Column(String(128))
    food_type = Column(SmallInteger)
    max_durability = Column(Integer)
    duration = Column(Integer)
    material = Column(Integer)
    sheath = Column(Integer)


class Item(Object):

    id = Column(Integer, primary_key=True)

    @declared_attr
    def item_template_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:world_db")}.{ItemTemplate.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    stack_count = Column(Integer, default=1)

    item_template = relationship('ItemTemplate', lazy='subquery')

    @hybrid_property
    def object_type(self):
        return ObjectType.ITEM.value

    @hybrid_property
    def type_mask(self):
        return TypeMask.ITEM.value

    @hybrid_property
    def high_guid(self):
        return HighGuid.HIGHGUID_ITEM.value

    @hybrid_property
    def guid(self):
        # item id equals to Mangos low_guid property
        if self.id and self.item_template.entry:
            return self.id | (self.item_template.entry << 24) | (self.high_guid << 48)
        else:
            raise Exception(
                '[Item/model]: id and entry should exists, id={}, entry={}'.format(
                    self.id, self.item_template.entry
                )
            )
