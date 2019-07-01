import asyncio
from concurrent.futures import TimeoutError

from Utils.Debug.Logger import Logger
from Utils.Timer import Timer
from World.Region.RegionManager import RegionManager


class WorldManager(object):

    def __init__(self):
        self.heartbeat = 1
        self.last_update = None
        self.region_mgr = RegionManager()

    async def run(self):
        while True:
            self.last_update = Timer.get_ms_time()

            try:
                await asyncio.wait_for(self.update(), timeout=1.0)
            except TimeoutError:
                Logger.warning('[World Manager]: Timeout...')
            except Exception as e:
                Logger.error('[World Manager]: another exception "{}"'.format(e))
            finally:
                await asyncio.sleep(self.heartbeat)

    async def update(self):
        try:
            await self.region_mgr.refresh()
        except Exception as e:
            Logger.error('[World Manager]: on update "{}"'.format(e))
