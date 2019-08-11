from World.Object.Constants.UpdateObjectFields import ObjectField
from World.Update.Constants.ObjectUpdateType import ObjectUpdateType
from World.Update.UpdatePacketBatch import UpdatePacketBatch
from World.Update.UpdatePacket import UpdatePacket
from DB.Connection.RealmConnection import RealmConnection
from World.Object.model import Object
from World.Object.Unit.Movement.Movement import Movement
from Utils.Debug.Logger import Logger


class ObjectManager(object):

    def __init__(self, **kwargs):
        self.update_packet_builder = UpdatePacketBatch()
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

    def build_update_packet(self, fields: list):
        update_packet = UpdatePacket(
            self.world_object,
            self.object_update_type,
            self.world_object.object_type,
            self.movement
        )

        for field in fields:
            update_packet.add_field(field, self.get_object_field(field))

        batch = update_packet.update(send_packed_guid=True)
        self.add_batch(batch)

        return self

    def add_batch(self, batch):
        # this method can be used for add external packets (from another managers) to current packet
        self.update_packet_builder.add_packet(batch)
        return self

    # ignore build arg if you need batch instead of update packet
    def get_update_packet(self, build=False):
        return self.update_packet_builder.get_packet(build)

    # inheritable
    def init_movement(self):
        self.movement.object_type = self.world_object.object_type
        self.movement.high_guid = self.world_object.high_guid

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
        return self

    # enter/exit are safe, should be used instead of __del__
    def __enter__(self):
        connection = RealmConnection()
        self.session = connection.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return True
