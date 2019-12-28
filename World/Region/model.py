from sqlalchemy.orm import relationship
from sqlalchemy import orm

from DB.BaseModel import BaseModel
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
    def init_on_load(self) -> None:
        self.octree = None

    # we can detect NPC by unit_template field which is NULL for players and NOT NULL for NPC
    units = relationship('Unit', primaryjoin="and_((Region.id == Unit.region_id), (Unit.unit_template_id))")

    players = relationship('Player', lazy='joined')

    def get_octree(self) -> OctreeNode:
        return self.octree

    def set_octree(self, node: OctreeNode) -> None:
        self.octree = node


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
