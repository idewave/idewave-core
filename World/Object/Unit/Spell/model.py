from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String

from DB.BaseModel import WorldModel

from Config.Run.config import Config


class SpellTemplate(WorldModel):

    id = Column(Integer, primary_key=True)
    entry = Column(Integer, unique=True)
    name = Column(String(128))
    cost = Column(Integer)
    school = Column(Integer)
    range = Column(Integer)


class DefaultSpell(WorldModel):

    id = Column(Integer, primary_key=True)
    race = Column(Integer, nullable=True)
    char_class = Column(Integer, nullable=True)

    spell_template_id = Column(
        Integer,
        ForeignKey(
            f'{Config.Database.DBNames.world_db}.{SpellTemplate.__tablename__}.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )
    spell_template = relationship('SpellTemplate')
