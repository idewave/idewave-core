import io
from struct import unpack

from World.Object.Unit.Constants.MovementFlags import MovementFlags
from World.Object.Unit.Movement.Movement import Movement
from Server.Registry.QueuesRegistry import QueuesRegistry

from Utils.Debug.Logger import Logger


class MovementHandler(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.opcode = int.from_bytes(packet[2:6], 'little')

        self.movement = Movement()

        self.temp_ref = kwargs.pop('temp_ref', None)
        if self.temp_ref is None:
            raise Exception('[Movement Handler]: temp_ref does not exists')

    async def process(self):
        self._parse_packet()

        player = self.temp_ref.player
        player.position = self.movement.position

        await QueuesRegistry.movement_queue.put((player, self.movement))

        return None, None

    def _parse_packet(self):
        buf = io.BytesIO(self.packet[6:])

        self.movement.movement_flags = MovementHandler._set_movement_flags(buf.read(4))
        self.movement.movement_flags2 = int.from_bytes(buf.read(1), 'little')

        self.movement.time = buf.read(4)

        self.movement.position.x = unpack('<f', buf.read(4))[0]
        self.movement.position.y = unpack('<f', buf.read(4))[0]
        self.movement.position.z = unpack('<f', buf.read(4))[0]
        self.movement.position.orientation = unpack('<f', buf.read(4))[0]

        if self.movement.movement_flags & MovementFlags.ONTRANSPORT.value:
            self.movement.transport_guid = buf.read(8)
            self.movement.transport_position.x = unpack('<f', buf.read(4))[0]
            self.movement.transport_position.y = unpack('<f', buf.read(4))[0]
            self.movement.transport_position.z = unpack('<f', buf.read(4))[0]
            self.movement.transport_time = buf.read(4)

        if self.movement.movement_flags & MovementFlags.SWIMMING.value:
            self.movement.swim_pitch = unpack('<f', buf.read(4))[0]

        self.movement.fall_time = unpack('<f', buf.read(4))[0]

    @staticmethod
    def _set_movement_flags(value):
        data = int.from_bytes(value, 'little')
        if MovementFlags.has_value(data):
            return MovementFlags(data).value
        else:
            return MovementFlags.NONE.value
