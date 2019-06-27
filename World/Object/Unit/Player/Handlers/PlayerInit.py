from World.Object.Unit.Player.PlayerManager import PlayerManager
from Config.Run.queues import connections_queue


class PlayerInit(object):

    ''' Just creates Player for using in another handlers '''

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)
        self.reader = kwargs.pop('reader', None)
        self.writer = kwargs.pop('writer', None)
        self.header_crypt = kwargs.pop('header_crypt', None)

    async def process(self):
        self._load_player()
        await connections_queue.put((self.temp_ref.player.name, self.reader, self.writer, self.header_crypt))
        return None, None

    def _load_player(self):
        # size (first 2 bytes) - opcode (next 4 bytes) - guid (remaining bytes)
        guid = int.from_bytes(self.packet[6:], 'little')
        player_mgr = PlayerManager().load(id=guid)

        self.temp_ref.player = player_mgr.player
