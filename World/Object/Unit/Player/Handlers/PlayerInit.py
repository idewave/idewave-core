from World.Object.Unit.Player.PlayerManager import PlayerManager
from Server.Registry.QueuesRegistry import QueuesRegistry


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

        await QueuesRegistry.connections_queue.put((
            self.temp_ref.player.name,
            self.reader, self.writer,
            self.header_crypt
        ))
        await QueuesRegistry.players_queue.put(self.temp_ref.player)

        return None, None

    def _load_player(self):
        # size (first 2 bytes) - opcode (next 4 bytes) - guid (remaining bytes)
        guid = int.from_bytes(self.packet[6:], 'little')
        with PlayerManager() as player_mgr:
            player_mgr.load(id=guid)
            self.temp_ref.player = player_mgr.player
