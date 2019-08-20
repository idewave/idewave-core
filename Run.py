import asyncio
import subprocess

from colorama import init

from Server.LoginServer import LoginServer
from Server.WorldServer import WorldServer
from Server.WebsocketServer.WebsocketServer import WebsocketServer

from Server.Registry.QueuesRegistry import QueuesRegistry
from World.WorldManager import WorldManager
from Server.Queue.MultiProcessQueue import MultiProcessQueue

from Utils.Debug.Logger import Logger


if __name__ == '__main__':
    # initialize colorama for make ansi codes works in Windows
    init()

    loop = asyncio.get_event_loop()

    login_server = LoginServer.create()
    world_server = WorldServer.create()
    websocket_server = WebsocketServer.create()

    world_manager = WorldManager()

    QueuesRegistry.web_data_queue = MultiProcessQueue.get_instance()
    QueuesRegistry.players_queue = asyncio.Queue()
    QueuesRegistry.movement_queue = asyncio.Queue()
    QueuesRegistry.connections_queue = asyncio.Queue()
    QueuesRegistry.update_packets_queue = asyncio.Queue()

    # TODO: check how this works for windows
    subprocess.run('redis-server --daemonize yes', shell=True)

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
        pass
    except Exception as e:
        Logger.error('[Run]: (run forever) {}'.format(e))
        raise e
    finally:
        loop.close()
