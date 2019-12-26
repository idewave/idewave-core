from World.Object.Unit.Player.PlayerManager import PlayerManager
from Server.Registry.QueuesRegistry import QueuesRegistry
from Server.Connection.Connection import Connection

from Utils.Debug.Logger import Logger


class PlayerInit(object):

    __slots__ = ('data', 'connection')

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        self._load_player()

        await QueuesRegistry.connections_queue.put(self.connection)
        # await QueuesRegistry.players_queue.put(self.connection.player)
        # await QueuesRegistry.broadcast_callback_queue.put(self._broadcast)
        Logger.notify(f"[Player Init]: {self.connection.player.guid}")

        return None, None

    def _load_player(self) -> None:
        # size (first 2 bytes) - opcode (next 4 bytes) - guid (remaining bytes)
        guid = int.from_bytes(self.data, 'little')
        with PlayerManager() as player_mgr:
            player_mgr.load(id=guid)
            player = player_mgr.player
            self.connection.player = player
