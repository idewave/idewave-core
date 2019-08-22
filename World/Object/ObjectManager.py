from World.Object.model import Object
from World.Object.Constants.UpdateObjectFields import ObjectField
from World.WorldPacket.UpdatePacket.Constants.ObjectUpdateType import ObjectUpdateType
from World.WorldPacket.UpdatePacket.Builders.UpdatePacketBuilder import UpdatePacketBuilder
from World.Object.Unit.Movement.Movement import Movement
from DB.Connection.RealmConnection import RealmConnection

from Utils.Debug.Logger import Logger


class ObjectManager(object):

    MAX_UPDATE_PACKETS_INCLUDED = 15

    def __init__(self, **kwargs):
        self.update_packet_builder = None
        self.fields = {}

        self.object_update_type = ObjectUpdateType.CREATE_OBJECT.value
        self.movement = Movement()

        self.world_object = Object()

    def find(self, **kwargs):
        self.world_object = self.session.query(self.__class__).filter_by(**kwargs).first()
        return self

    def find_all(self, **kwargs):
        return self.session.query(self.__class__).filter_by(**kwargs).all()

    def save(self):
        self.session.add(self.world_object)
        self.session.commit()
        return self

    def delete(self, **kwargs):
        self.session.query(Object).filter_by(**kwargs).delete()
        return self

    def get_object_field(self, field):
        if field in self.fields:
            return self.fields.get(field)
        else:
            return 0

    def set_object_field(self, field, value):
        self.fields[field] = value

    def add_object_fields(self):
        self.set_object_field(ObjectField.GUID, self.world_object.guid)
        self.set_object_field(ObjectField.TYPE, self.world_object.type_mask)
        self.set_object_field(ObjectField.ENTRY, self.world_object.entry)
        self.set_object_field(ObjectField.SCALE_X, self.world_object.scale_x)

    def set_object_update_type(self, object_update_type: ObjectUpdateType):
        self.object_update_type = object_update_type.value

    def create_batch(self, fields: list):
        for field in fields:
            self.update_packet_builder.add_field(field, self.get_object_field(field))

        return self.update_packet_builder.create_batch(send_packed_guid=True)

    def add_batch(self, batch: bytes):
        # this method also can be used for adding batches from another managers
        self.update_packet_builder.add_batch(batch)
        return self

    def build_update_packet(self):
        self.update_packet_builder.build()
        return self

    def get_update_packets(self):
        return self.update_packet_builder.get_packets()

    # inheritable
    def init_movement(self):
        self.movement.set_object_type(self.world_object.object_type)
        self.movement.set_high_guid(self.world_object.high_guid)

    def set_movement(self, movement: Movement):
        self.movement = movement

    # overridable
    def load(self, **kwargs):
        id = kwargs.pop('id')
        self.world_object = self.session.query(Object).filter_by(id=id).first()
        return self

    # overridable
    def new(self, **kwargs):
        return self

    def set(self, world_object: Object):
        self.world_object = world_object
        return self

    # inheritable
    def prepare(self):
        # init data for UpdatePacket
        self.add_object_fields()
        self.init_movement()

        self.update_packet_builder = UpdatePacketBuilder(
            update_object=self.world_object,
            update_type=self.object_update_type,
            object_type=self.world_object.object_type,
            movement=self.movement
        )

        return self

    # enter/exit are safe, should be used instead of __del__
    def __enter__(self):
        connection = RealmConnection()
        self.session = connection.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return True
