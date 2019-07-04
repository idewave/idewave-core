import asyncio
from concurrent.futures import TimeoutError

from Utils.Debug.Logger import Logger
from Utils.Timer import Timer
from World.Object.Unit.Player.model import Player
from World.Region.RegionManager import RegionManager
from Server.Registry.QueuesRegistry import QueuesRegistry


class WorldManager(object):

    def __init__(self):
        self.heartbeat = 1
        self.last_update = None
        self.region_mgr = RegionManager()

    async def run(self):
        while True:
            self.last_update = Timer.get_ms_time()

            try:
                player = await asyncio.wait_for(QueuesRegistry.players_queue.get(), timeout=1.0)
                await asyncio.wait_for(self.update(player), timeout=1.0)
            except TimeoutError:
                pass
            except Exception as e:
                Logger.error('[World Manager]: another exception "{}"'.format(e))
            finally:
                await asyncio.sleep(self.heartbeat)

    async def update(self, player: Player):
        await self.region_mgr.refresh_players(player)
        await self.region_mgr.refresh_creatures()
