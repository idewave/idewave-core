from sqlalchemy import Column, Integer, String

from World.Object.StaticObject.model import StaticObject
from DB.BaseModel import WorldModel


class ContainerTemplate(WorldModel):

    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class Container(StaticObject):

    id = Column(Integer, primary_key=True)
