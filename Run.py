import asyncio
import subprocess
import traceback
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

from Server.LoginServer import LoginServer
from Server.WorldServer import WorldServer
from Server.WebServer import WebServer
from Server.Wrapper.QueuesRegistry import QueuesRegistry
from World.WorldManager import WorldManager
from Server.Queue.MultiProcessQueue import MultiProcessQueue

from Utils.Debug.Logger import Logger


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    login_server = LoginServer.create()
    world_server = WorldServer.create()

    QueuesRegistry.web_data_queue = MultiProcessQueue.get_instance()
    QueuesRegistry.players_queue = asyncio.Queue()
    QueuesRegistry.connections_queue = asyncio.Queue()
    QueuesRegistry.update_packets_queue = asyncio.Queue()

    executor = ProcessPoolExecutor(max_workers=cpu_count())

    # TODO: check how this works for windows
    subprocess.run('redis-server --daemonize yes', shell=True)

    try:
        loop.run_until_complete(
            asyncio.gather(
                login_server.get_instance(),

                world_server.get_instance(),
                asyncio.ensure_future(world_server.refresh_connections()),
                asyncio.ensure_future(world_server.send_update_packet_to_player()),

                # FIXME: anti-pattern
                # https://stackoverflow.com/questions/49275895/asyncio-multiple-concurrent-servers/49280706#49280706
                loop.run_in_executor(executor, WebServer.run),

                asyncio.ensure_future(WorldManager().run())
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
        pass

    loop.close()
