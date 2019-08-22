import asyncio

from Utils.Timer import Timer
from World.Region.RegionManager import RegionManager
from Server.Registry.QueuesRegistry import QueuesRegistry


class WorldManager(object):

    def __init__(self):
        self.heartbeat = 0.01
        self.last_update = None
        self.region_mgr = RegionManager()

    async def run(self):
        while True:
            self.last_update = Timer.get_ms_time()

            self._register_tasks()

            await asyncio.sleep(self.heartbeat)

            # try:
            #     player = QueuesRegistry.players_queue.get_nowait()
            #     self.update(player)
            # except asyncio.QueueEmpty:
            #     pass
            # except MemoryError:
            #     Logger.error('[World Mgr]: MemoryError')
            #     gc.collect()
            #     del gc.garbage[:]
            #     pass
            # except Exception as e:
            #     Logger.error('[World Manager]: another exception "{}"'.format(e))
            #     traceback.print_exc()
            # finally:
            #     try:
            #         # await QueuesRegistry.web_data_queue.put(self.region_mgr.get_regions_as_json())
            #         await asyncio.sleep(self.heartbeat)
            #     except Exception as e:
            #         Logger.error('[World Manager]: {}'.format(e))
            #         traceback.print_exc()

    # def update(self, player: Player):
    #     asyncio.ensure_future(self.region_mgr.refresh_players(player))
    #     asyncio.ensure_future(self.region_mgr.refresh_creatures())

    async def process_player_enter_world(self):
        try:
            player = QueuesRegistry.players_queue.get_nowait()
        except asyncio.QueueEmpty:
            return
        else:
            self.region_mgr.add_player(player)
        finally:
            await asyncio.sleep(0.01)

    async def process_player_movement(self):
        try:
            player, movement = QueuesRegistry.movement_queue.get_nowait()
        except asyncio.QueueEmpty:
            return
        else:
            self.region_mgr.update_player_movement(player, movement)
        finally:
            await asyncio.sleep(0.01)

    async def process_player_exit_world(self):
        try:
            player = QueuesRegistry.remove_player_queue.get_nowait()
        except asyncio.QueueEmpty:
            return
        else:
            self.region_mgr.remove_player(player)
        finally:
            await asyncio.sleep(0.01)

    def _register_tasks(self):
        asyncio.gather(
            asyncio.ensure_future(self.process_player_enter_world()),
            asyncio.ensure_future(self.process_player_movement()),
            asyncio.ensure_future(self.process_player_exit_world()),
        )
