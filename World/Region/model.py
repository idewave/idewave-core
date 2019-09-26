from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy import orm
from typing import Union

from DB.BaseModel import BaseModel
from World.Object.Unit.model import Unit
from World.Object.Unit.Player.model import Player
from World.Region.Octree.OctreeNode import OctreeNode

from Config.Run.config import Config


class Region(BaseModel):

    id                      = BaseModel.column(type='integer', primary_key=True)
    identifier              = BaseModel.column(type='integer', unique=True)
    y1                      = BaseModel.column(type='float')
    y2                      = BaseModel.column(type='float')
    x1                      = BaseModel.column(type='float')
    x2                      = BaseModel.column(type='float')
    map_id                  = BaseModel.column(type='mediumint')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }

    def __init__(self):
        self.octree = None

    # this uses on session.query() etc
    @orm.reconstructor
    def init_on_load(self):
        self.octree = None

    # we can detect NPC by unit_template field which is NULL for players and NOT NULL for NPC
    units = relationship('Unit', primaryjoin="and_((Region.id == Unit.region_id), (Unit.unit_template_id))")

    players = relationship('Player', lazy='joined')

    def get_octree(self) -> OctreeNode:
        return self.octree

    def set_octree(self, node: OctreeNode) -> None:
        self.octree = node

    # @hybrid_property
    # # objects with POSITION: containers; units; players etc
    # def objects_registry(self):
    #     return self._registry
    #
    # @hybrid_method
    # def get_object(self, guid: int):
    #     if self.is_object_exists(guid):
    #         return self.objects_registry[guid]
    #
    # @hybrid_method
    # def is_object_exists(self, guid: int):
    #     return guid in self.objects_registry and self.objects_registry[guid] is not None
    #
    # @hybrid_method
    # def set_object(self, guid: int, value: Union[Unit, Player]):
    #     self.objects_registry[guid] = value
    #
    # @hybrid_method
    # def remove_object(self, guid: int):
    #     if self.is_object_exists(guid):
    #         del self._registry[guid]

    # @hybrid_method
    # def get_online_players(self):
    #     return self.online_players
    #
    # @hybrid_method
    # def update_player(self, player: Player):
    #     self.online_players[player.name] = player
    #
    # @hybrid_method
    # def remove_player(self, player: Player):
    #     if player.name in self.online_players:
    #         del self.online_players[player.name]
    #
    # @hybrid_method
    # def get_online_player_by_guid(self, guid: int):
    #     for name in self.online_players:
    #         if self.online_players[name].guid == guid:
    #             return self.online_players[name]


class DefaultLocation(BaseModel):

    __tablename__ = 'default_location'

    id                  = BaseModel.column(type='integer', primary_key=True)
    x                   = BaseModel.column(type='float')
    y                   = BaseModel.column(type='float')
    z                   = BaseModel.column(type='float')
    map_id              = BaseModel.column(type='mediumint')

    race                = BaseModel.column(type='integer')

    region_id           = BaseModel.column(type='integer', foreign_key=Config.Database.DBNames.world_db + '.region.id')

    region              = relationship('Region', lazy='subquery')

    __table_args__ = {
        'schema': Config.Database.DBNames.world_db
    }
