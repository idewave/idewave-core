import asyncio
import subprocess
import traceback

from multiprocessing import cpu_count

from Server.LoginServer import LoginServer
from Server.WorldServer import WorldServer
from Server.WebsocketServer.WebsocketServer import WebsocketServer

from Server.Registry.QueuesRegistry import QueuesRegistry
from World.WorldManager import WorldManager
from Server.Queue.MultiProcessQueue import MultiProcessQueue

from Utils.Debug.Logger import Logger


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    login_server = LoginServer.create()
    world_server = WorldServer.create()
    websocket_server = WebsocketServer.create()

    world_manager = WorldManager()

    QueuesRegistry.web_data_queue = MultiProcessQueue.get_instance()
    QueuesRegistry.players_queue = asyncio.Queue()
    QueuesRegistry.connections_queue = asyncio.Queue()
    QueuesRegistry.update_packets_queue = asyncio.Queue()

    # TODO: check how this works for windows
    subprocess.run('redis-server --daemonize yes', shell=True)

    try:
        loop.run_until_complete(
            asyncio.gather(
                login_server.get_instance(),

                world_server.get_instance(),
                # asyncio.ensure_future(world_server.refresh_connections()),
                # asyncio.ensure_future(world_server.send_update_packet_to_player()),

                websocket_server.get_instance(),
                # asyncio.ensure_future(websocket_server.get_web_data()),

                asyncio.ensure_future(world_manager.run())
            )
        )
    except Exception as e:
        Logger.error('[Run]: {}'.format(e))
        traceback.print_exc()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        Logger.error('[Run]: {}'.format(e))
        traceback.print_exc()
        pass
    finally:
        loop.close()
