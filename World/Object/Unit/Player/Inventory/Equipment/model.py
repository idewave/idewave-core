from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey

from DB.BaseModel import RealmModel, WorldModel
from World.Object.Unit.Player.model import Player
from World.Object.Item.model import Item, ItemTemplate


class Equipment(RealmModel):

    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)

    @declared_attr
    def item_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:realm_db")}.{Item.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    @declared_attr
    def player_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:realm_db")}.{Player.__tablename__}.id',
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

    @declared_attr
    def item_template_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:world_db")}.{ItemTemplate.__tablename__}.id'
            )
        )

    item_template = relationship('ItemTemplate')
