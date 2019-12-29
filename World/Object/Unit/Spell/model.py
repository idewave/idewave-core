from sqlalchemy.orm import relationship

from DB.BaseModel import BaseModel

from Config.Run.config import Config


class SpellTemplate(BaseModel):

    __tablename__ = 'spell_template'

    id                      = BaseModel.column(type='integer', primary_key=True)
    entry                   = BaseModel.column(type='integer', unique=True)
    name                    = BaseModel.column(type='string')
    cost                    = BaseModel.column(type='integer')
    school                  = BaseModel.column(type='integer')
    range                   = BaseModel.column(type='integer')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }


class DefaultSpell(BaseModel):

    __tablename__ = 'default_spell'

    race                    = BaseModel.column(type='integer', nullable=True)
    char_class              = BaseModel.column(type='integer', nullable=True)

    spell_template_id = BaseModel.column(type='integer',
                                         foreign_key=Config.Database.DBNames.world_db + '.spell_template.id')
    spell_template = relationship('SpellTemplate')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }