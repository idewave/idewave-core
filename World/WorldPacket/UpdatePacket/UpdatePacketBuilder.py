from struct import pack

from World.WorldPacket.UpdatePacket.Constants.ObjectUpdateType import ObjectUpdateType
from World.WorldPacket.UpdatePacket.UpdateBlocksBuilder import UpdateBlocksBuilder


class UpdatePacketBuilder(object):

    MAX_UPDATE_PACKETS_AS_ONE = 15

    TYPES_WITH_OBJECT_TYPE = (
        ObjectUpdateType.CREATE_OBJECT.value,
        ObjectUpdateType.CREATE_OBJECT2.value
    )

    TYPES_WITH_MOVEMENT = (
        ObjectUpdateType.MOVEMENT.value,
        ObjectUpdateType.CREATE_OBJECT.value,
        ObjectUpdateType.CREATE_OBJECT2.value,
    )

    TYPES_WITH_MISC = (
        ObjectUpdateType.CREATE_OBJECT.value,
        ObjectUpdateType.CREATE_OBJECT2.value,
    )

    TYPES_WITH_FIELDS = (
        ObjectUpdateType.VALUES.value,
        ObjectUpdateType.MOVEMENT.value,
        ObjectUpdateType.CREATE_OBJECT.value,
        ObjectUpdateType.CREATE_OBJECT2.value
    )

    IMPLEMENTED_TYPES = (
        ObjectUpdateType.MOVEMENT.value,
        ObjectUpdateType.CREATE_OBJECT.value,
        ObjectUpdateType.CREATE_OBJECT2.value
    )

    def __init__(self, **kwargs):
        self.update_object = kwargs.pop('update_object')
        self.update_type = kwargs.pop('update_type')
        self.object_type = kwargs.pop('object_type')
        self.movement = kwargs.pop('movement')
        self.update_blocks_builder = UpdateBlocksBuilder()

        # self.packet = bytes()
        self.batches = []
        self.packets = []

    def _has_fields(self):
        return self.update_type in self.TYPES_WITH_FIELDS

    def add_field(self, field, value, offset=0):
        # using offset for fields with size more than 1
        # for example for SKILL_INFO_1_ID
        if self._has_fields():
            self.update_blocks_builder.add(field, value, offset)

    def create_batch(self, send_packed_guid=False):
        guid = pack('<Q', self.update_object.guid)
        mask = bytes()

        if send_packed_guid:
            guid = self.update_object.packed_guid
        else:
            # 0xff means that guid is not compressed
            mask = pack('<B', 0xff)

        header = pack(
            '<B',
            self.update_type,
        )

        header += mask + guid

        object_type = bytes()
        if self.update_type in self.TYPES_WITH_OBJECT_TYPE:
            object_type = pack(
                '<B',
                self.object_type
            )

        object_movement = bytes()
        if self.update_type in self.TYPES_WITH_MOVEMENT:
            object_movement = self.movement.to_bytes()

        builder_data = bytes()
        if self.update_type in self.TYPES_WITH_FIELDS:
            builder_data = self.update_blocks_builder.to_bytes()

        packet = header + object_type + object_movement + builder_data

        return packet

    def add_batch(self, batch: bytes):
        self.batches.append(batch)

    def build(self):
        # TODO: should be fixed according to transport existing
        has_transport = int(False)

        while self.batches:
            head_update_packet = self.batches.pop(0)
            count = 1
            for index in range(0, UpdatePacketBuilder.MAX_UPDATE_PACKETS_AS_ONE):
                if not self.batches:
                    break

                batch = self.batches.pop(0)
                head_update_packet += batch
                count += 1

            header = pack(
                '<IB',
                count,
                has_transport
            )

            self.packets.append(header + head_update_packet)

    def get_packets(self):
        return self.packets
