import asyncio

from colorama import init

from Server.LoginServer import LoginServer
from Server.WorldServer import WorldServer
# from Server.WebsocketServer.WebsocketServer import WebsocketServer

from Server.Registry.QueuesRegistry import QueuesRegistry
from World.WorldManager import WorldManager
from World.Region.RegionManager import RegionManager

from Utils.Debug.Logger import Logger


if __name__ == '__main__':
    # initialize colorama for make ansi codes works in Windows
    init()

    loop = asyncio.get_event_loop()

    login_server = LoginServer.create()
    world_server = WorldServer.create()
    # websocket_server = WebsocketServer.create()

    # region_manager = RegionManager()
    # region_tasks = [
    #     asyncio.ensure_future(RegionManager.refresh_region(region))
    #     for region in region_manager.regions
    # ]

    # world_manager = WorldManager()

    # QueuesRegistry.web_data_queue = MultiProcessQueue.get_instance()

    QueuesRegistry.session_keys_queue = asyncio.Queue()
    QueuesRegistry.players_queue = asyncio.Queue()
    QueuesRegistry.remove_player_queue = asyncio.Queue()
    QueuesRegistry.connections_queue = asyncio.Queue()
    QueuesRegistry.disconnect_queue = asyncio.Queue()

    QueuesRegistry.packets_queue = asyncio.Queue()

    # TODO: remove redundant queues
    # QueuesRegistry.update_packets_queue = asyncio.Queue()
    #
    # QueuesRegistry.movement_queue = asyncio.Queue()
    # QueuesRegistry.movement_packets_queue = asyncio.Queue()
    #
    # QueuesRegistry.text_message_queue = asyncio.Queue()
    # QueuesRegistry.text_message_packets_queue = asyncio.Queue()
    #
    # QueuesRegistry.name_query_queue = asyncio.Queue()
    # QueuesRegistry.name_query_packets_queue = asyncio.Queue()

    try:
        loop.run_until_complete(
            asyncio.gather(
                login_server.get_instance(),
                world_server.get_instance(),
                # websocket_server.get_instance(),
                # asyncio.ensure_future(world_manager.run())
            )
        )
    except Exception as e:
        Logger.error('[Run]: (run until complete) {}'.format(e))
        raise e

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # TODO: add signal to stop all runned tasks
        pass
    except Exception as e:
        Logger.error('[Run]: (run forever) {}'.format(e))
        raise e
    finally:
        loop.close()
