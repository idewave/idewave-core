from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import orm

from DB.BaseModel import BaseModel
from World.Object.Unit.Player.model import Player

from Config.Run.config import Config


class Region(BaseModel):

    id                      = BaseModel.column(type='integer', primary_key=True)
    # TODO: region_id should be renamed, too vague
    region_id               = BaseModel.column(type='integer', unique=True)
    y1                      = BaseModel.column(type='float')
    y2                      = BaseModel.column(type='float')
    x1                      = BaseModel.column(type='float')
    x2                      = BaseModel.column(type='float')
    map_id                  = BaseModel.column(type='mediumint')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }

    def __init__(self):
        self.online_players = {}

    # this uses on session.query() etc
    @orm.reconstructor
    def init_on_load(self):
        self.online_players = {}

    # specify only creatures, we can detect them by unit_template field which is NULL for players and NOT NULL for NPC
    units = relationship('Unit', primaryjoin="and_((Region.id == Unit.region_id), (Unit.unit_template_id))")

    players = relationship('Player', lazy='joined')

    @hybrid_method
    def get_online_players(self):
        return self.online_players

    @hybrid_method
    def set_online_players(self, player: Player):
        if player.region.id == self.id:
            self.online_players[player.name] = player
        else:
            if player.name in self.online_players:
                del self.online_players[player.name]
