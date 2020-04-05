from typing import List, AnyStr
from os import urandom
from asyncio.streams import StreamReader, StreamWriter
from asyncio import (
    TimeoutError,
    ensure_future,
    wait_for,
    sleep,
    gather
)

from Server import BaseServer, Connection, QueuesRegistry
from Utils.Debug import Logger
from World.WorldPacket import WorldOpCode, WorldPacketManager
from World.Observer import WorldObserver
from Config.Run.config import Config


class WorldServer(BaseServer):

    __slots__ = (
        'session_keys',
        'connections',
        'world_observer'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_keys = {}
        self.connections = {}
        self.world_observer: WorldObserver = kwargs.pop('world_observer')

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        self._register_tasks()

        connection = Connection(reader=reader, writer=writer, session_keys=self.session_keys)
        world_packet_mgr = WorldPacketManager(
            connection=connection,
            world_observer=self.world_observer
        )

        # send auth challenge
        auth_seed: bytes = urandom(4)
        writer.write(
            world_packet_mgr.generate_packet(
                WorldOpCode.SMSG_AUTH_CHALLENGE,
                auth_seed
            )
        )

        connection.auth_seed = auth_seed

        while True:
            try:
                await WorldServer.process_request(reader, writer, world_packet_mgr)
            except TimeoutError:
                continue
            finally:
                await sleep(Config.Realm.Settings.min_timeout)

    @staticmethod
    async def process_request(reader: StreamReader, writer: StreamWriter, world_packet_mgr: WorldPacketManager):
        request: bytes = await wait_for(reader.read(4096), timeout=Config.Realm.Settings.min_timeout)
        if request:
            size, opcode, data = request[:2], request[2:6], request[6:]

            response: List[bytes] = await wait_for(
                world_packet_mgr.process(
                    size=size,
                    opcode=opcode,
                    data=data
                ),
                timeout=Config.Realm.Settings.min_timeout
            )

            if response:
                for packet in response:
                    writer.write(packet)
                    await writer.drain()

    def _register_tasks(self):
        gather(
            ensure_future(self.add_connection()),
            ensure_future(self.remove_connection()),
            ensure_future(self.add_session_keys()),
            ensure_future(self.broadcast_packets()),
        )

    async def add_connection(self):
        while True:
            connection: Connection = await QueuesRegistry.connections_queue.get()
            self.connections[connection.player.name] = connection
            Logger.info('[World Server]: added connection for player "{}"'.format(connection.player.name))
            await sleep(Config.Realm.Settings.min_timeout)

    async def remove_connection(self):
        while True:
            player_name: AnyStr = await QueuesRegistry.disconnect_queue.get()
            if self.connections.get(player_name):
                del self.connections[player_name]
                Logger.info('[World Server]: player "{}" disconnected'.format(player_name))

    async def add_session_keys(self):
        while True:
            key, value = await QueuesRegistry.session_keys_queue.get()
            self.session_keys[key] = value
            await sleep(Config.Realm.Settings.min_timeout)

    async def broadcast_packets(self):
        while True:
            try:
                player_name, opcode, data = await wait_for(
                    QueuesRegistry.packets_queue.get(),
                    timeout=Config.Realm.Settings.min_timeout
                )
            except TimeoutError:
                pass
            else:
                connection: Connection = self.connections.get(player_name, None)
                if connection:
                    writer: StreamWriter = connection.writer

                    response: bytes = WorldPacketManager(
                        connection=connection
                    ).generate_packet(
                        opcode=opcode,
                        data=data,
                    )

                    writer.write(response)
                    await writer.drain()
            finally:
                await sleep(Config.Realm.Settings.min_timeout)

    @staticmethod
    def create(**kwargs):
        Logger.info('[World Server]: init')

        return WorldServer(
            host=Config.Realm.Connection.WorldServer.host,
            port=Config.Realm.Connection.WorldServer.port,
            world_observer=kwargs.pop('world_observer')
        )
