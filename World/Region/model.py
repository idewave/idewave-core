from sqlalchemy.orm import relationship

from DB.BaseModel import BaseModel

from Config.Run.config import Config


class Region(BaseModel):

    id                      = BaseModel.column(type='integer', primary_key=True)
    region_id               = BaseModel.column(type='integer', unique=True)
    y1                      = BaseModel.column(type='float')
    y2                      = BaseModel.column(type='float')
    x1                      = BaseModel.column(type='float')
    x2                      = BaseModel.column(type='float')
    map_id                  = BaseModel.column(type='mediumint')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }

    # specify only creatures, we can detect them by unit_template field which is NULL for players and NOT NULL for NPC
    units = relationship('Unit', primaryjoin="and_((Region.id == Unit.region_id), (Unit.unit_template_id))")

    players = relationship('Player', lazy='joined')
