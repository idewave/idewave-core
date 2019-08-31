from sqlalchemy.orm import relationship

from DB.BaseModel import BaseModel

from Config.Run.config import Config


class SkillTemplate(BaseModel):

    __tablename__ = 'skill_template'

    id                      = BaseModel.column(type='integer', primary_key=True)
    entry                   = BaseModel.column(type='integer', unique=True)
    name                    = BaseModel.column(type='string')
    min                     = BaseModel.column(type='integer')
    max                     = BaseModel.column(type='integer')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }


class DefaultSkill(BaseModel):

    __tablename__ = 'default_skill'

    race                    = BaseModel.column(type='integer', nullable=True)
    char_class              = BaseModel.column(type='integer', nullable=True)

    skill_template_id       = BaseModel.column(type='integer',
                                         foreign_key=Config.Database.DBNames.world_db + '.skill_template.id')

    skill_template          = relationship('SkillTemplate')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }