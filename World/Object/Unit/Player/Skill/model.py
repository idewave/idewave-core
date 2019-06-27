from DB.BaseModel import BaseModel

from Config.Run.config import Config


class SkillTemplate(BaseModel):

    __tablename__ = 'skill_template'

    id                      = BaseModel.column(type='integer', primary_key=True)
    entry                   = BaseModel.column(type='integer')
    name                    = BaseModel.column(type='string')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }