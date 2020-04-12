from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey, String

from DB.BaseModel import WorldModel


class SkillTemplate(WorldModel):

    id = Column(Integer, primary_key=True)
    entry = Column(Integer, unique=True)
    name = Column(String(128))
    min = Column(Integer)
    max = Column(Integer)


class DefaultSkill(WorldModel):

    id = Column(Integer, primary_key=True)
    race = Column(Integer, nullable=True)
    char_class = Column(Integer, nullable=True)

    @declared_attr
    def skill_template_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:world_db")}.{SkillTemplate.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    skill_template = relationship('SkillTemplate')
