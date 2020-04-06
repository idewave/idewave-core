from sqlalchemy import Column, Integer

from World.Object.model import ObjectWithPosition
from DB.BaseModel import WorldModel


class TransportTemplate(WorldModel):

    id = Column(Integer, primary_key=True)


class Transport(ObjectWithPosition):

    id = Column(Integer, primary_key=True)
