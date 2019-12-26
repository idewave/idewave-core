from asyncio import QueueEmpty, ensure_future, sleep, gather

from Utils.Timer import Timer
from World.Region.RegionManager import RegionManager
from Server.Registry.QueuesRegistry import QueuesRegistry
from Server.Constants.ServerContants import MIN_TIMEOUT

from Utils.Debug.Logger import Logger


class WorldManager(object):

    __slots__ = ('last_update', 'region_mgr')

    def __init__(self):
        self.last_update = None
        self.region_mgr = RegionManager()

    async def run(self):
        while True:
            self.last_update = Timer.get_ms_time()
            self._register_tasks()

            await sleep(MIN_TIMEOUT)

    def _register_tasks(self):
        gather(
            ensure_future(self.process_broadcast()),
        )

    async def process_broadcast(self):
        try:
            opcode, packets, callback = QueuesRegistry.broadcast_callback_queue.get_nowait()
        except QueueEmpty:
            return
        else:
            self.region_mgr.broadcast(opcode, packets, callback)

    # @staticmethod
    # async def process_player_enter_world():
    #     try:
    #         player = QueuesRegistry.players_queue.get_nowait()
    #     except QueueEmpty:
    #         return
    #     else:
    #         RegionManager.add_player(player)
    #
    # async def process_player_exit_world(self):
    #     try:
    #         player = QueuesRegistry.remove_player_queue.get_nowait()
    #     except QueueEmpty:
    #         return
        # else:
        #     self.region_mgr.remove_player(player)

    # async def process_player_movement(self):
    #     try:
    #         player, opcode, packet = QueuesRegistry.movement_queue.get_nowait()
    #     except asyncio.QueueEmpty:
    #         return
    #     else:
    #         self.region_mgr.update_player_movement(player, opcode, packet)
    #     finally:
    #         await asyncio.sleep(0.01)

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
