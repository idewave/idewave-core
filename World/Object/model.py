from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, Float

from DB.BaseModel import RealmModel
from World.Object.Constants import (
    TypeMask,
    ObjectType
)


class Object(RealmModel):

    __abstract__ = True

    entry = Column(Integer)
    display_id = Column(Integer)

    @hybrid_property
    def object_type(self) -> int:
        return ObjectType.OBJECT.value

    @hybrid_property
    def type_mask(self) -> int:
        return TypeMask.OBJECT.value

    @hybrid_property
    def high_guid(self):
        return None

    @hybrid_property
    def guid(self) -> int:
        _guid = self.id

        if hasattr(self, 'low_guid'):
            _guid = self.low_guid | (self.high_guid << 48)

            if bool(self.entry):
                _guid = (self.low_guid |
                         (self.entry << 24) |
                         (self.high_guid << 48))

        return _guid

    @hybrid_property
    def packed_guid(self) -> bytes:
        pack_guid = bytearray(8 + 1)
        size = 1
        index = 0

        guid = self.guid

        while guid:
            if guid & 0xff > 0:
                pack_guid[0] |= (1 << index)
                pack_guid[size] = guid & 0xff
                size += 1

            index += 1
            guid >>= 8

        return bytes(pack_guid[:size])


class ObjectWithPosition(Object):

    __abstract__ = True

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    orientation = Column(Float)
    map_id = Column(Integer)

    @declared_attr
    def scale_x(self):
        return Column(Float, default=self.from_config("object:default:scale_x"))
