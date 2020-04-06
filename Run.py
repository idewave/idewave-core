import asyncio

from colorama import init

from Server.LoginServer import LoginServer
from Server.WorldServer import WorldServer
# from Server.WebsocketServer.WebsocketServer import WebsocketServer

from Server.Registry.QueuesRegistry import QueuesRegistry
from World.WorldManager import WorldManager
from World.Region.RegionManager import RegionManager

from World.Observer import WorldObserver
from World.Observer.Constants import *

from Utils.Debug import Logger


if __name__ == '__main__':
    # initialize colorama for make ansi codes works in Windows
    init()

    loop = asyncio.get_event_loop()

    world_observer = WorldObserver(handlers_map={
        CHANGE_POSITION: [],
        WEATHER_SET_FINE: [],
        WEATHER_SET_RAIN: [],
        WEATHER_SET_SNOW: [],
        WEATHER_SET_STORM: [],
        WEATHER_SET_THUNDERS: [],
        WEATHER_SET_BLACK_RAIN: [],
    }, coverage=RegionManager().regions)

    login_server = LoginServer.create()
    world_server = WorldServer.create(world_observer=world_observer)
    # websocket_server = WebsocketServer.create()

    # region_manager = RegionManager()
    # region_tasks = [
    #     asyncio.ensure_future(RegionManager.refresh_region(region))
    #     for region in region_manager.regions
    # ]

    world_manager = WorldManager()

    # QueuesRegistry.web_data_queue = MultiProcessQueue.get_instance()

    QueuesRegistry.session_keys_queue = asyncio.Queue()
    QueuesRegistry.players_queue = asyncio.Queue()
    QueuesRegistry.remove_player_queue = asyncio.Queue()
    QueuesRegistry.connections_queue = asyncio.Queue()
    QueuesRegistry.disconnect_queue = asyncio.Queue()

    QueuesRegistry.packets_queue = asyncio.Queue()
    QueuesRegistry.broadcast_packets_queue = asyncio.Queue()
    # QueuesRegistry.broadcast_callback_queue = asyncio.Queue()

    try:
        loop.run_until_complete(
            asyncio.gather(
                login_server.get_instance(),
                world_server.get_instance(),
                # websocket_server.get_instance(),
                asyncio.ensure_future(world_manager.run())
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
