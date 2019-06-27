from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from DB.BaseModel import BaseModel
from World.Object.model import Object
from World.Object.Constants.TypeMask import TypeMask
from World.Object.Constants.ObjectType import ObjectType
from World.Object.Constants.HighGuid import HighGuid

from Config.Run.config import Config


class ItemTemplate(BaseModel):

    __tablename__ = 'item_template'

    id                      = BaseModel.column(type='integer', primary_key=True)
    entry                   = BaseModel.column(type='integer', unique=True)
    item_class              = BaseModel.column(type='integer')
    item_subclass           = BaseModel.column(type='integer')
    name                    = BaseModel.column(type='string')
    display_id              = BaseModel.column(type='mediumint')
    quality                 = BaseModel.column(type='tinyint')
    flags                   = BaseModel.column(type='integer')
    buy_count               = BaseModel.column(type='tinyint')
    buy_price               = BaseModel.column(type='integer')
    sell_price              = BaseModel.column(type='integer')
    item_type               = BaseModel.column(type='tinyint')
    allowable_class         = BaseModel.column(type='mediumint')
    allowable_race          = BaseModel.column(type='mediumint')
    item_level              = BaseModel.column(type='tinyint')
    required_level          = BaseModel.column(type='tinyint')
    required_skill          = BaseModel.column(type='integer')
    required_skill_rank     = BaseModel.column(type='integer')
    required_spell          = BaseModel.column(type='integer')
    maxcount                = BaseModel.column(type='smallint')
    stackable               = BaseModel.column(type='smallint')
    container_slots         = BaseModel.column(type='tinyint')
    stat_type1              = BaseModel.column(type='tinyint')
    stat_value1             = BaseModel.column(type='smallint')
    stat_type2              = BaseModel.column(type='tinyint')
    stat_value2             = BaseModel.column(type='smallint')
    stat_type3              = BaseModel.column(type='tinyint')
    stat_value3             = BaseModel.column(type='smallint')
    stat_type4              = BaseModel.column(type='tinyint')
    stat_value4             = BaseModel.column(type='smallint')
    stat_type5              = BaseModel.column(type='tinyint')
    stat_value5             = BaseModel.column(type='smallint')
    stat_type6              = BaseModel.column(type='tinyint')
    stat_value6             = BaseModel.column(type='smallint')
    stat_type7              = BaseModel.column(type='tinyint')
    stat_value7             = BaseModel.column(type='smallint')
    stat_type8              = BaseModel.column(type='tinyint')
    stat_value8             = BaseModel.column(type='smallint')
    stat_type9              = BaseModel.column(type='tinyint')
    stat_value9             = BaseModel.column(type='smallint')
    stat_type10             = BaseModel.column(type='tinyint')
    stat_value10            = BaseModel.column(type='smallint')
    dmg_min1                = BaseModel.column(type='float')
    dmg_max1                = BaseModel.column(type='float')
    dmg_type1               = BaseModel.column(type='tinyint')
    dmg_min2                = BaseModel.column(type='float')
    dmg_max2                = BaseModel.column(type='float')
    dmg_type2               = BaseModel.column(type='tinyint')
    dmg_min3                = BaseModel.column(type='float')
    dmg_max3                = BaseModel.column(type='float')
    dmg_type3               = BaseModel.column(type='tinyint')
    dmg_min4                = BaseModel.column(type='float')
    dmg_max4                = BaseModel.column(type='float')
    dmg_type4               = BaseModel.column(type='tinyint')
    dmg_min5                = BaseModel.column(type='float')
    dmg_max5                = BaseModel.column(type='float')
    dmg_type5               = BaseModel.column(type='tinyint')
    armor                   = BaseModel.column(type='smallint')
    fire_res                = BaseModel.column(type='tinyint')
    nature_res              = BaseModel.column(type='tinyint')
    frost_res               = BaseModel.column(type='tinyint')
    shadow_res              = BaseModel.column(type='tinyint')
    arcane_res              = BaseModel.column(type='tinyint')
    delay                   = BaseModel.column(type='smallint', default=1000)
    description             = BaseModel.column(type='string')
    food_type               = BaseModel.column(type='tinyint')
    max_durability          = BaseModel.column(type='integer')
    duration                = BaseModel.column(type='integer')
    material                = BaseModel.column(type='integer')
    sheath                  = BaseModel.column(type='integer')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }


class Item(Object):

    id                      = Object.column(type='integer',
                                            foreign_key=Config.Database.DBNames.realm_db + '.object.id',
                                            primary_key=True)

    item_template_id        = Object.column(type='integer',
                                               foreign_key=Config.Database.DBNames.world_db + '.item_template.id')

    stack_count             = Object.column(type='integer', default=1)

    object                  = relationship('Object', lazy='subquery')
    item_template           = relationship('ItemTemplate', lazy='subquery')

    __table_args__ = {
        'schema': Config.Database.DBNames.realm_db
    }

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
                '[Item/model]: id and entry should exists, id={}, entry={}'.format(self.id, self.item_template.entry)
            )
