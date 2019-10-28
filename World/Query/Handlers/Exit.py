from World.Object.Unit.Player.PlayerManager import PlayerManager
from Server.Registry.QueuesRegistry import QueuesRegistry

from Server.Connection.Connection import Connection


class Exit(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        # TODO: correctly process disconnect
        with PlayerManager() as player_mgr:
            player_mgr.set(self.connection.player).save()

        await QueuesRegistry.disconnect_queue.put(self.connection.player.name)
        await QueuesRegistry.remove_player_queue.put(self.connection.player)

        return None, None
