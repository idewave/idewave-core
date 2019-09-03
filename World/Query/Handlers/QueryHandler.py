from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode

from Utils.Timer import Timer
from Server.Registry.QueuesRegistry import QueuesRegistry


class QueryHandler(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.opcode = WorldOpCode(int.from_bytes(packet[2:6], 'little'))
        self.temp_ref = kwargs.pop('temp_ref', None)

        if self.temp_ref is None:
            raise Exception('[QueryHandler]: temp ref does not exists')

        self.player = self.temp_ref.player

    async def process(self):
        if self.opcode == WorldOpCode.CMSG_NAME_QUERY:
            # we send this to show player info for another players; to allow chat
            guid = int.from_bytes(self.packet[6:14], 'little')

            await QueuesRegistry.name_query_queue.put((self.player, guid))

            name_bytes = self.player.name.encode('utf-8') + b'\x00'
            response = pack(
                '<Q{name_len}sB3IB'.format(name_len=len(name_bytes)),
                self.player.guid,
                name_bytes,
                0,
                self.player.race,
                self.player.gender,
                self.player.char_class,
                0
            )
            return WorldOpCode.SMSG_NAME_QUERY_RESPONSE, response

        elif self.opcode == WorldOpCode.CMSG_QUERY_TIME:
            response = pack(
                '<2I',
                Timer.get_ms_time(),
                0
            )
            return WorldOpCode.SMSG_QUERY_TIME_RESPONSE, response

        else:
            return None, None
