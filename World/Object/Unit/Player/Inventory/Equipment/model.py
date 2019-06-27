from sqlalchemy.orm import relationship

from World.Object.Item.model import Item
from DB.BaseModel import BaseModel

from Config.Run.config import Config


class Equipment(BaseModel):

    ''' Contains equipment for each player '''

    item_id             = Item.column(type='integer',
                                        foreign_key=Config.Database.DBNames.realm_db + '.item.id')

    player_id           = Item.column(type='integer',
                                        foreign_key=Config.Database.DBNames.realm_db + '.player.id')

    slot_id             = Item.column(type='integer')

    durability          = Item.column(type='integer')

    item                = relationship('Item', lazy='subquery')
    player              = relationship('Player', lazy='subquery')

    __table_args__ = {
        'schema': Config.Database.DBNames.realm_db
    }


class DefaultEquipment(BaseModel):

    __tablename__       = 'default_equipment'

    race                = BaseModel.column(type='integer')
    char_class          = BaseModel.column(type='integer')


    item_template_id    = BaseModel.column(type='integer',
                                           foreign_key=Config.Database.DBNames.world_db + '.item_template.id')
    item_template       = relationship('ItemTemplate')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }
