import io

from struct import unpack

from World.Object.Unit.Movement.Constants.MovementFlags import MovementFlags
from World.Object.Position import Position
from Server.Registry.QueuesRegistry import QueuesRegistry

from Server.Connection.Connection import Connection


class MovementHandler(object):

    def __init__(self, **kwargs):
        self.opcode = kwargs.pop('opcode')
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

        self.movement_flags = MovementFlags.NONE.value
        self.movement_flags2 = 0
        self.time = 0
        self.position = Position()
        self.transport_guid = 0
        self.transport_position = Position()
        self.transport_time = 0
        self.swim_pitch = float(0)
        self.fall_time = 0
        self.jump_velocity = float(0)
        self.jump_sin_angle = float(0)
        self.jump_cos_angle = float(0)
        self.jump_x_y_speed = float(0)

    async def process(self):
        self._parse_packet()

        if self._is_movement_valid():
            player = self.connection.player
            player.position = self.position

            await QueuesRegistry.movement_queue.put((player, self.opcode, self.data))

        return None, None

    def _is_movement_valid(self):
        return True

    def _parse_packet(self):
        buf = io.BytesIO(self.data)

        self.movement_flags = MovementHandler._set_movement_flags(buf.read(4))
        self.movement_flags2 = int.from_bytes(buf.read(1), 'little')

        self.time = buf.read(4)

        self.position.x = unpack('<f', buf.read(4))[0]
        self.position.y = unpack('<f', buf.read(4))[0]
        self.position.z = unpack('<f', buf.read(4))[0]
        self.position.orientation = unpack('<f', buf.read(4))[0]

        if self.movement_flags & MovementFlags.ONTRANSPORT.value:
            self.transport_guid = buf.read(8)
            self.transport_position.x = unpack('<f', buf.read(4))[0]
            self.transport_position.y = unpack('<f', buf.read(4))[0]
            self.transport_position.z = unpack('<f', buf.read(4))[0]
            self.transport_time = buf.read(4)

        if self.movement_flags & MovementFlags.SWIMMING.value:
            self.swim_pitch = unpack('<f', buf.read(4))[0]

        if self.movement_flags & MovementFlags.FALLING.value:
            self.jump_velocity = unpack('<f', buf.read(4))[0]
            self.jump_sin_angle = unpack('<f', buf.read(4))[0]
            self.jump_cos_angle = unpack('<f', buf.read(4))[0]
            self.jump_x_y_speed = unpack('<f', buf.read(4))[0]

        self.fall_time = unpack('<f', buf.read(4))[0]

    @staticmethod
    def _set_movement_flags(value):
        data = int.from_bytes(value, 'little')
        if MovementFlags.has_value(data):
            return MovementFlags(data).value
        else:
            return MovementFlags.NONE.value
