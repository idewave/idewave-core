from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import orm
from typing import List

from DB.BaseModel import BaseModel
from World.Object.Constants.TypeMask import TypeMask
from World.Object.Constants.ObjectType import ObjectType

from Config.Run.config import Config


class Object(BaseModel):

    id                      = BaseModel.column(type='integer', primary_key=True)
    entry                   = BaseModel.column(type='integer')
    scale_x                 = BaseModel.column(type='float', default=Config.World.Object.Defaults.scale_x)

    __table_args__ = {
        'schema': Config.Database.DBNames.realm_db
    }

    def __init__(self):
        self._tracked_guids = set()

    # this uses on session.query() etc
    @orm.reconstructor
    def init_on_load(self):
        self._tracked_guids = set()

    @hybrid_property
    def object_type(self):
        return ObjectType.OBJECT.value

    @hybrid_property
    def type_mask(self):
        return TypeMask.OBJECT.value

    @hybrid_property
    def high_guid(self):
        return None

    @hybrid_property
    def guid(self):
        _guid = self.id

        if hasattr(self, 'low_guid'):
            _guid = self.low_guid | (self.high_guid << 48)

            if bool(self.entry):
                _guid = (self.low_guid |
                         (self.entry << 24) |
                         (self.high_guid << 48))

        return _guid

    @hybrid_property
    def packed_guid(self):
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

    @hybrid_property
    def tracked_guids(self):
        # objects in 'update_dist' radius, see Config.yml
        return self._tracked_guids

    @tracked_guids.setter
    def tracked_guids(self, guids: List[int]):
        self._tracked_guids = guids
