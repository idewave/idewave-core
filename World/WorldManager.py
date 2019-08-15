import asyncio
import traceback
import gc

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
                player = QueuesRegistry.players_queue.get_nowait()
                self.update(player)
            except asyncio.QueueEmpty:
                pass
            except MemoryError:
                Logger.error('[World Mgr]: MemoryError')
                gc.collect()
                del gc.garbage[:]
                pass
            except Exception as e:
                Logger.error('[World Manager]: another exception "{}"'.format(e))
                traceback.print_exc()
            finally:
                try:
                    # await QueuesRegistry.web_data_queue.put(self.region_mgr.get_regions_as_json())
                    await asyncio.sleep(self.heartbeat)
                except Exception as e:
                    Logger.error('[World Manager]: {}'.format(e))
                    traceback.print_exc()

    def update(self, player: Player):
        asyncio.ensure_future(self.region_mgr.refresh_players(player))
        asyncio.ensure_future(self.region_mgr.refresh_creatures())
