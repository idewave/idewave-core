from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection

from Utils.Timer import Timer
from Server.Registry.QueuesRegistry import QueuesRegistry


class QueryHandler(object):

    def __init__(self, **kwargs):
        self.opcode = kwargs.pop('opcode')
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        if self.opcode == WorldOpCode.CMSG_NAME_QUERY:
            # we send this to show player info for another players; to allow chat
            guid = int.from_bytes(self.data[:8], 'little')

            await QueuesRegistry.name_query_queue.put((self.connection.player, guid))

            name_bytes = self.connection.player.name.encode('utf-8') + b'\x00'
            response = pack(
                '<Q{name_len}sB3IB'.format(name_len=len(name_bytes)),
                self.connection.player.guid,
                name_bytes,
                0,
                self.connection.player.race,
                self.connection.player.gender,
                self.connection.player.char_class,
                0
            )
            return WorldOpCode.SMSG_NAME_QUERY_RESPONSE, [response]

        elif self.opcode == WorldOpCode.CMSG_QUERY_TIME:
            response = pack(
                '<2I',
                Timer.get_ms_time(),
                0
            )
            return WorldOpCode.SMSG_QUERY_TIME_RESPONSE, [response]

        else:
            return None, None
