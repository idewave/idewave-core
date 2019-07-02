from struct import unpack

from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Region.RegionManager import RegionManager

from Utils.Debug.Logger import Logger


class ZoneUpdate(object):

    def __init__(self, packet: bytes, **kwargs):
        # sometimes with packet some garbage receives, so need to cut the packet
        self.packet = packet[:10]
        self.temp_ref = kwargs.pop('temp_ref', None)
        if self.temp_ref is None:
            raise Exception('[Zone Update]: temp_ref does not exists')

    async def process(self):
        region_id = unpack('<I', self.packet[-4:])[0]

        if not self.temp_ref.player.region.region_id == region_id:
            with RegionManager() as region_mgr:
                region = region_mgr.get_region(region_id=region_id)
                self.temp_ref.player.region = region

            with PlayerManager() as player_mgr:
                player_mgr.set(self.temp_ref.player).save()
                Logger.notify('[Zone Update]: saving player')

        return None, None
