from sqlalchemy.orm import relationship
from sqlalchemy import orm, Column, Integer, Float, ForeignKey

from DB.BaseModel import WorldModel
from World.Region.Octree.Node import ChildNode
from Config.Run.config import Config


class Region(WorldModel):

    id = Column(Integer, primary_key=True)
    identifier = Column(Integer, unique=True)
    y1 = Column(Float)
    y2 = Column(Float)
    x1 = Column(Float)
    x2 = Column(Float)
    map_id = Column(Integer)

    def __init__(self):
        self.octree = None

    # this uses on session.query() etc
    @orm.reconstructor
    def init_on_load(self) -> None:
        self.octree = None

    # we can detect NPC by unit_template field which is NULL for players and NOT NULL for NPC
    units = relationship(
        'Unit',
        primaryjoin="and_((Region.id == Unit.region_id), (Unit.unit_template_id))"
    )

    players = relationship('Player', lazy='joined')

    def get_octree(self) -> ChildNode:
        return self.octree

    def set_octree(self, node: ChildNode) -> None:
        self.octree = node


class DefaultLocation(WorldModel):

    id = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    map_id = Column(Integer)

    race = Column(Integer)

    region_id = Column(
        Integer,
        ForeignKey(
            f'{Config.Database.DBNames.world_db}.{Region.__tablename__}.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )

    region = relationship('Region', lazy='subquery')
