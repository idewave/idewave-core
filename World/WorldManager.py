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

            # self._register_tasks()

            await asyncio.sleep(self.heartbeat)

    def _register_tasks(self):
        # tasks = [asyncio.ensure_future(RegionManager.refresh_region(region)) for region in self.region_mgr.regions]
        asyncio.gather(
            asyncio.ensure_future(WorldManager.process_player_enter_world()),
            # asyncio.ensure_future(self.process_player_movement()),
            # asyncio.ensure_future(self.process_player_exit_world()),
            # asyncio.ensure_future(self.process_chat_message()),
            # asyncio.ensure_future(self.process_name_query()),
        )

    @staticmethod
    async def process_player_enter_world():
        try:
            player = QueuesRegistry.players_queue.get_nowait()
        except asyncio.QueueEmpty:
            return
        else:
            RegionManager.add_player(player)
        finally:
            await asyncio.sleep(0.01)

    # async def process_player_movement(self):
    #     try:
    #         player, opcode, packet = QueuesRegistry.movement_queue.get_nowait()
    #     except asyncio.QueueEmpty:
    #         return
    #     else:
    #         self.region_mgr.update_player_movement(player, opcode, packet)
    #     finally:
    #         await asyncio.sleep(0.01)

    async def process_player_exit_world(self):
        try:
            player = QueuesRegistry.remove_player_queue.get_nowait()
        except asyncio.QueueEmpty:
            return
        else:
            self.region_mgr.remove_player(player)
        finally:
            await asyncio.sleep(0.01)

    # async def process_chat_message(self):
    #     try:
    #         sender, text_message_packet = QueuesRegistry.text_message_queue.get_nowait()
    #     except asyncio.QueueEmpty:
    #         return
    #     else:
    #         self.region_mgr.send_chat_message(sender, text_message_packet)
    #     finally:
    #         await asyncio.sleep(0.01)
    #
    # async def process_name_query(self):
    #     try:
    #         requester, target_guid = QueuesRegistry.name_query_queue.get_nowait()
    #     except asyncio.QueueEmpty:
    #         return
    #     else:
    #         self.region_mgr.send_name_query(requester, target_guid)
    #     finally:
    #         await asyncio.sleep(0.01)
