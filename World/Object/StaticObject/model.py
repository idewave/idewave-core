from sqlalchemy import Column, Integer, String

from World.Object.model import ObjectWithPosition
from DB.BaseModel import WorldModel


class StaticObjectTemplate(WorldModel):

    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class StaticObject(ObjectWithPosition):

    id = Column(Integer, primary_key=True)
