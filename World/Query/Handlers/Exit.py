from World.Object.Unit.Player.PlayerManager import PlayerManager
from Server.Registry.QueuesRegistry import QueuesRegistry


class Exit(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)
        if self.temp_ref is None:
            raise Exception('[Exit]: temp_ref does not exists')

    async def process(self):
        # TODO: correctly process disconnect
        with PlayerManager() as player_mgr:
            player_mgr.set(self.temp_ref.player).save()

        await QueuesRegistry.disconnect_queue.put(self.temp_ref.player.name)
        await QueuesRegistry.remove_player_queue.put(self.temp_ref.player)

        return None, None
