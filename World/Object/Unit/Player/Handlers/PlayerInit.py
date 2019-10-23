from World.Object.Unit.Player.PlayerManager import PlayerManager
from Server.Registry.QueuesRegistry import QueuesRegistry
from Server.Connection.Connection import Connection

from Exceptions.Wrappers.ProcessException import ProcessException


class PlayerInit(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        self._load_player()

        await QueuesRegistry.connections_queue.put(self.connection)
        await QueuesRegistry.players_queue.put(self.connection.player)

        return None, None

    @ProcessException
    def _load_player(self) -> None:
        # size (first 2 bytes) - opcode (next 4 bytes) - guid (remaining bytes)
        guid = int.from_bytes(self.data, 'little')
        with PlayerManager(connection=self.connection) as player_mgr:
            player_mgr.load(id=guid)
            self.connection.player = player_mgr.player
