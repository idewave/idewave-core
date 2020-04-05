from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

from DB.BaseModel import RealmModel, WorldModel
from World.Object.Unit.Player.model import Player
from World.Object.Item.model import Item, ItemTemplate

from Config.Run.config import Config


class Equipment(RealmModel):

    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)

    item_id = Column(
        Integer,
        ForeignKey(
            f'{Config.Database.DBNames.realm_db}.{Item.__tablename__}.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )

    player_id = Column(
        Integer,
        ForeignKey(
            f'{Config.Database.DBNames.realm_db}.{Player.__tablename__}.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )

    slot_id = Column(Integer)

    durability = Column(Integer)

    item = relationship('Item', lazy='subquery')
    player = relationship('Player', lazy='subquery')


class DefaultEquipment(WorldModel):

    __tablename__ = 'default_equipment'

    id = Column(Integer, primary_key=True)

    race = Column(Integer)
    char_class = Column(Integer)

    item_template_id = Column(
        Integer,
        ForeignKey(
            f'{Config.Database.DBNames.world_db}.{ItemTemplate.__tablename__}.id'
        )
    )
    item_template = relationship('ItemTemplate')
