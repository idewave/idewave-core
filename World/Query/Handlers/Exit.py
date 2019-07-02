from World.Object.Unit.Player.PlayerManager import PlayerManager


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
        return None, None
