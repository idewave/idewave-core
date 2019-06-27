from struct import pack

from World.Object.Position import Position
from World.Object.Unit.Constants.MovementFlags import MovementFlags
from World.Object.Unit.JumpData import JumpData
from World.Object.Constants.UpdateObjectFlags import UpdateObjectFlags
from World.Object.Constants.ObjectType import ObjectType
from Utils.Timer import Timer
from Utils.Debug.Logger import Logger

from Config.Run.config import Config


class Movement(object):

    def __init__(self):
        self.update_flags = (
            UpdateObjectFlags.UPDATEFLAG_LIVING.value |
            UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value |
            UpdateObjectFlags.UPDATEFLAG_HIGHGUID.value |
            UpdateObjectFlags.UPDATEFLAG_SELF.value
        )

        self.object_type = None

        self.time = 0
        self.position = Position()
        self.transport_guid = 0
        self.transport_position = Position()
        self.swim_pitch = float(0)
        self.jump_data = JumpData()
        self.spline_elevation_unk = float(0)

        # guids
        self.low_guid = None
        self.high_guid = None

    def set_update_flags(self, update_flags: int):
        self.update_flags = update_flags

    def set_object_type(self, object_type):
        self.object_type = object_type

    def set_guids(self, low_guid, high_guid):
        self.low_guid = low_guid
        self.high_guid = high_guid

    def to_bytes(self):
        data = bytes()

        move_flags = MovementFlags.NONE.value

        data += pack('<B', self.update_flags)

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_LIVING.value:
            # TODO: get actual movement flags
            if self.object_type == ObjectType.PLAYER.value:
                # TODO: check for transport
                move_flags &= ~MovementFlags.ONTRANSPORT.value
            elif self.object_type == ObjectType.UNIT.value:
                move_flags &= ~MovementFlags.ONTRANSPORT.value

            data += pack(
                '<IBI',
                move_flags,
                0,
                Timer.get_ms_time()
            )

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_HAS_POSITION.value:
            # TODO: check if transport
            data += self.position.to_bytes()

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_LIVING.value:
            # TODO: check transport, swimming and flying
            data += pack('<I', 0)               # last fall time

            movement = Config.World.Object.Unit.Player.Defaults.Movement

            data += pack(
                '<8f',
                movement.speed_walk,
                movement.speed_run,
                movement.speed_run_back,
                movement.speed_swim,
                movement.speed_swim_back,
                movement.speed_flight,
                movement.speed_flight_back,
                movement.speed_turn
            )

        if self.update_flags & UpdateObjectFlags.UPDATEFLAG_LOWGUID.value:
            if self.object_type == ObjectType.ITEM.value:
                data += pack('<I', self.low_guid)
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
                data += pack('<I', self.high_guid)
            else:
                data += pack('<I', 0x00000000) # high guid for unit or player

        return data
