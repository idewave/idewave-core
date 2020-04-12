from struct import pack
from typing import Dict

from World.WorldPacket.UpdatePacket.Constants.ObjectUpdateType import ObjectUpdateType
from World.WorldPacket.UpdatePacket.Builders.UpdateBlocksBuilder import UpdateBlocksBuilder
from World.Object.Unit.Movement.Constants.MovementFlags import MovementFlags
from World.Object.Constants.UpdateObjectFlags import UpdateObjectFlags
from World.Object.Constants.ObjectType import ObjectType
from Typings.Abstract.AbstractBuilder import AbstractBuilder
from Utils.Timer import Timer


class UpdatePacketBuilder(AbstractBuilder):

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

        self.update_flags = None
        self.movement_flags = MovementFlags.NONE.value
        self.movement_flags2 = 0

        self.update_object = kwargs.pop('update_object')
        self.update_type = kwargs.pop('update_type')
        self.object_type = kwargs.pop('object_type')
        self.update_blocks_builder = UpdateBlocksBuilder()

        # 1 for TRANSPORT: zeppelins, ships, elevators etc
        self.has_transport: int = kwargs.pop('has_transport', 0)

        self.batches = []
        self.packets = []

    def _has_fields(self) -> bool:
        return self.update_type in self.TYPES_WITH_FIELDS

    def add_field(self, field, value, offset=0):
        # using offset for fields with size more than 1
        # for example for SKILL_INFO_1_ID
        if self._has_fields():
            self.update_blocks_builder.add(field, value, offset)

    def create_batch(self, send_packed_guid=False) -> bytes:
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
            object_movement = self._get_movement_info()

        builder_data = bytes()
        if self.update_type in self.TYPES_WITH_FIELDS:
            builder_data = self.update_blocks_builder.build()

        packet = header + object_type + object_movement + builder_data

        return packet

    def set_update_flags(self, update_flags: int) -> None:
        self.update_flags = update_flags

    def _get_movement_info(self) -> bytes:
        data = bytes()

        data += pack('<B', self.update_flags)

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_LIVING.value:
            if self.object_type == ObjectType.PLAYER.value:
                # TODO: check for transport
                self.movement_flags &= ~MovementFlags.ONTRANSPORT.value
            elif self.object_type == ObjectType.UNIT.value:
                self.movement_flags &= ~MovementFlags.ONTRANSPORT.value

            data += pack(
                '<IBI',
                self.movement_flags,
                self.movement_flags2,
                Timer.get_ms_time()
            )

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value:
            # TODO: check if transport
            data += self.update_object.position.build()

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_LIVING.value:
            # TODO: check transport, swimming and flying
            data += pack('<I', 0)  # last fall time

            movement_speed: Dict[str, float] = UpdatePacketBuilder.from_config('player:movement:speed')

            data += pack(
                '<8f',
                movement_speed['walk'],
                movement_speed['run'],
                movement_speed['run_back'],
                movement_speed['swim'],
                movement_speed['swim_back'],
                movement_speed['flight'],
                movement_speed['flight_back'],
                movement_speed['turn']
            )

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_LOWGUID.value:
            if self.object_type == ObjectType.ITEM.value:
                data += pack('<I', self.update_object.low_guid)
            elif self.object_type == ObjectType.UNIT.value:
                data += pack('<I', 0x0000000B)
            elif self.object_type == ObjectType.PLAYER.value:
                if self.update_flags & UpdateObjectFlags.UPDATEFLAG_SELF.value:
                    data += ('<I', 0x00000015)
                else:
                    data += ('<I', 0x00000008)
            else:
                data += ('<I', 0x00000000)

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value:
            # TODO: get high guid for another object types
            if self.object_type == ObjectType.ITEM.value:
                data += pack('<I', self.update_object.high_guid)
            else:
                data += pack('<I', 0x00000000)  # high guid for unit or player

        return data

    def add_batch(self, batch: bytes):
        self.batches.append(batch)

    def build(self) -> None:
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
                self.has_transport
            )

            self.packets.append(header + head_update_packet)

    def get_packets(self):
        return self.packets
