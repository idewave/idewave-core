import io
from struct import unpack

from World.Object.Unit.Constants.MovementFlags import MovementFlags
from World.Object.Position import Position
from Server.Registry.QueuesRegistry import QueuesRegistry


class MovementHandler(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.opcode = int.from_bytes(packet[2:6], 'little')
        self.move_flags = None
        self.move_flags2 = None
        self.time = 0
        self.position = Position()
        self.transport_guid = None
        self.transport_position = Position()
        self.transport_time = 0
        self.s_pitch = 0
        self.fall_time = 0

        self.temp_ref = kwargs.pop('temp_ref', None)
        if self.temp_ref is None:
            raise Exception('[Movement Handler]: temp_ref does not exists')

    async def process(self):
        self._parse_packet()

        player = self.temp_ref.player
        player.position = self.position
        await QueuesRegistry.players_queue.put(player)

        return None, None

    def _parse_packet(self):
        buf = io.BytesIO(self.packet[6:])

        self.move_flags = MovementHandler._set_move_flags(buf.read(4))
        self.move_flags2 = int.from_bytes(buf.read(1), 'little')
        self.time = buf.read(4)
        self.position.x = unpack('<f', buf.read(4))[0]
        self.position.y = unpack('<f', buf.read(4))[0]
        self.position.z = unpack('<f', buf.read(4))[0]
        self.position.orientation = unpack('<f', buf.read(4))[0]

        if self.move_flags & MovementFlags.ONTRANSPORT.value:
            self.transport_guid = buf.read(8)
            self.transport_position.x = unpack('<f', buf.read(4))[0]
            self.transport_position.y = unpack('<f', buf.read(4))[0]
            self.transport_position.z = unpack('<f', buf.read(4))[0]
            self.transport_time = buf.read(4)

        if self.move_flags & MovementFlags.SWIMMING.value:
            self.s_pitch = unpack('<f', buf.read(4))[0]

        self.fall_time = unpack('<f', buf.read(4))[0]

    @staticmethod
    def _set_move_flags(value):
        data = int.from_bytes(value, 'little')
        if MovementFlags.has_value(data):
            return MovementFlags(data).value
        else:
            return MovementFlags.NONE.value
