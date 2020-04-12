from struct import unpack

from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Region.RegionManager import RegionManager

from Server.Connection.Connection import Connection
from Typings.Abstract.AbstractHandler import AbstractHandler
from World.Observer.Constants import CHANGE_POSITION

from Utils.Debug import Logger


class ZoneUpdate(AbstractHandler):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        identifier = unpack('<I', self.data[:4])[0]

        player = self.connection.player

        if not player.region.identifier == identifier:
            old_region = player.region
            region = RegionManager().get_region(identifier=identifier)
            new_region = region
            player.region = region

            with PlayerManager() as player_mgr:
                player_mgr.set(player).save()
                Logger.notify(f'[Zone Update]: saving player "{player.name}"')
                player.notify(CHANGE_POSITION, {
                    'object': player,
                    'move_from': old_region,
                    'move_to': new_region
                })

        return None, None
