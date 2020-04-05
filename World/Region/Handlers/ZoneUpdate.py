from struct import unpack

from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Region.RegionManager import RegionManager

from Server.Connection.Connection import Connection
from Typings.Abstract import AbstractHandler

from Utils.Debug import Logger


class ZoneUpdate(AbstractHandler):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        identifier = unpack('<I', self.data[:4])[0]

        if not self.connection.player.region.identifier == identifier:
            region = RegionManager().get_region(identifier=identifier)
            self.connection.player.region = region

            with PlayerManager() as player_mgr:
                player_mgr.set(self.connection.player).save()
                Logger.notify('[Zone Update]: saving player')

        return None, None
