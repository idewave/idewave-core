import asyncio
import time

from asyncio.streams import StreamReader, StreamWriter
from os import urandom

from Server.BaseServer import BaseServer
from Utils.Debug.Logger import Logger
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Registry.QueuesRegistry import QueuesRegistry
from World.WorldPacket.WorldPacketManager import WorldPacketManager
from Server.Connection.Connection import Connection

from Exceptions.Wrappers.ProcessException import ProcessException

from Config.Run.config import Config


class WorldServer(BaseServer):

    __slots__ = ('session_keys', 'connections')

    def __init__(self, host, port):
        super().__init__(host, port)
        self.session_keys = {}
        self.connections = {}

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        self._register_tasks()

        connection = Connection(reader=reader, writer=writer, session_keys=self.session_keys)
        world_packet_mgr = WorldPacketManager(connection=connection)

        # send auth challenge
        auth_seed = urandom(4)
        writer.write(world_packet_mgr.generate_packet(WorldOpCode.SMSG_AUTH_CHALLENGE, auth_seed))

        connection.auth_seed = auth_seed

        while True:
            await self._process_request(reader, writer, world_packet_mgr)

    @ProcessException()
    async def _process_request(self, reader: StreamReader, writer: StreamWriter, world_packet_mgr: WorldPacketManager):
        request = await asyncio.wait_for(reader.read(4096), timeout=0.01)
        if request:
            size, opcode, data = request[:2], request[2:6], request[6:]

            response = await asyncio.wait_for(
                world_packet_mgr.process(size=size, opcode=opcode, data=data),
                timeout=0.01
            )

            if response:
                for packet in response:
                    writer.write(packet)
                    await writer.drain()

        await asyncio.sleep(0.01)

    def _register_tasks(self):
        asyncio.gather(
            asyncio.ensure_future(self.add_connection()),
            asyncio.ensure_future(self.remove_connection()),
            asyncio.ensure_future(self.add_session_keys()),
            # asyncio.ensure_future(self.send_dynamic_packets()),
            #
            # asyncio.ensure_future(self.send_update_packet_to_player()),
            # asyncio.ensure_future(self.send_movement_packet_to_player()),
            # asyncio.ensure_future(self.send_text_message_packet_to_player()),
            # asyncio.ensure_future(self.send_name_query_packet_to_player()),
        )

    @ProcessException()
    async def add_connection(self):
        while True:
            connection: Connection = await QueuesRegistry.connections_queue.get()
            self.connections[connection.player.name] = connection
            Logger.info('[World Server]: added connection for player "{}"'.format(connection.player.name))
            await asyncio.sleep(0.01)

    @ProcessException()
    async def remove_connection(self):
        while True:
            player_name = await QueuesRegistry.disconnect_queue.get()
            if self.connections.get(player_name):
                del self.connections[player_name]
                Logger.info('[World Server]: player "{}" disconnected'.format(player_name))

    @ProcessException()
    async def add_session_keys(self):
        while True:
            key, value = await QueuesRegistry.session_keys_queue.get()
            self.session_keys[key] = value
            await asyncio.sleep(0.01)

    # async def send_dynamic_packets(self):
    #     while True:
    #         try:
    #             player_name, packets, opcode = await asyncio.wait_for(
    #                 QueuesRegistry.dynamic_packets_queue.get(),
    #                 timeout=0.01
    #             )
    #         except TimeoutError:
    #             pass
    #         else:
    #             try:
    #                 connection = self.connections.get(player_name)
    #                 writer, header_crypt = None, None
    #
    #                 if connection:
    #                     writer = connection.get('writer')
    #                     header_crypt = connection.get('header_crypt')
    #             except KeyError:
    #                 # on login step player object not registered in self.connections,
    #                 # just ignore
    #                 pass
    #             else:
    #                 try:
    #                     for packet in packets:
    #                         response = WorldPacketManager.generate_packet(
    #                             opcode=opcode,
    #                             data=packet,
    #                             header_crypt=header_crypt
    #                         )
    #                         writer.write(response)
    #                         await writer.drain()
    #                 except BrokenPipeError:
    #                     del self.connections[player_name]
    #
    #                 except ConnectionResetError:
    #                     del self.connections[player_name]
    #         finally:
    #             await asyncio.sleep(0.01)

    # async def send_update_packet_to_player(self):
    #     while True:
    #         try:
    #             player_name, update_packets = await asyncio.wait_for(
    #                 QueuesRegistry.update_packets_queue.get(),
    #                 timeout=0.01
    #             )
    #         except TimeoutError:
    #             pass
    #         else:
    #             try:
    #                 writer = self.connections[player_name]['writer']
    #                 header_crypt = self.connections[player_name]['header_crypt']
    #             except KeyError:
    #                 # on login step player object not registered in self.connections,
    #                 # just ignore
    #                 pass
    #             else:
    #                 try:
    #                     for update_packet in update_packets:
    #                         response = WorldPacketManager.generate_packet(
    #                             opcode=WorldOpCode.SMSG_UPDATE_OBJECT,
    #                             data=update_packet,
    #                             header_crypt=header_crypt
    #                         )
    #                         Logger.test('Send update packet to {}'.format(player_name))
    #                         writer.write(response)
    #                         await writer.drain()
    #                 except BrokenPipeError:
    #                     del self.connections[player_name]
    #
    #                 except ConnectionResetError:
    #                     del self.connections[player_name]
    #         finally:
    #             await asyncio.sleep(0.01)
    #
    # async def send_movement_packet_to_player(self):
    #     while True:
    #         try:
    #             player_name, movement_packet, opcode = await asyncio.wait_for(
    #                 QueuesRegistry.movement_packets_queue.get(),
    #                 timeout=0.01
    #             )
    #             # player_name, movement_packet, opcode = QueuesRegistry.movement_packets_queue.get_nowait()
    #         # except asyncio.QueueEmpty:
    #         #     pass
    #         except TimeoutError:
    #             pass
    #         else:
    #             try:
    #                 writer = self.connections[player_name]['writer']
    #                 header_crypt = self.connections[player_name]['header_crypt']
    #             except KeyError:
    #                 # on login step player object not registered in self.connections,
    #                 # just ignore
    #                 pass
    #             else:
    #                 try:
    #                     response = WorldPacketManager.generate_packet(
    #                         opcode=opcode,
    #                         data=movement_packet,
    #                         header_crypt=header_crypt
    #                     )
    #                     writer.write(response)
    #                     await writer.drain()
    #                 except BrokenPipeError:
    #                     del self.connections[player_name]
    #
    #                 except ConnectionResetError:
    #                     del self.connections[player_name]
    #         finally:
    #             await asyncio.sleep(0.01)
    #
    # async def send_text_message_packet_to_player(self):
    #     while True:
    #         try:
    #             player_name, text_message_packet = await asyncio.wait_for(
    #                 QueuesRegistry.text_message_packets_queue.get(),
    #                 timeout=0.01
    #             )
    #         # except asyncio.QueueEmpty:
    #         #     pass
    #         except TimeoutError:
    #             pass
    #         else:
    #             try:
    #                 writer = self.connections[player_name]['writer']
    #                 header_crypt = self.connections[player_name]['header_crypt']
    #             except KeyError:
    #                 # on login step player object not registered in self.connections,
    #                 # just ignore
    #                 pass
    #             else:
    #                 try:
    #                     response = WorldPacketManager.generate_packet(
    #                         opcode=WorldOpCode.SMSG_MESSAGECHAT,
    #                         data=text_message_packet,
    #                         header_crypt=header_crypt
    #                     )
    #                     writer.write(response)
    #                     await writer.drain()
    #                 except BrokenPipeError:
    #                     del self.connections[player_name]
    #
    #                 except ConnectionResetError:
    #                     del self.connections[player_name]
    #         finally:
    #             await asyncio.sleep(0.01)
    #
    # async def send_name_query_packet_to_player(self):
    #     while True:
    #         try:
    #             player_name, name_query_packet = await asyncio.wait_for(
    #                 QueuesRegistry.name_query_packets_queue.get(),
    #                 timeout=0.01
    #             )
    #         # except asyncio.QueueEmpty:
    #         #     pass
    #         except TimeoutError:
    #             pass
    #         else:
    #             try:
    #                 writer = self.connections[player_name]['writer']
    #                 header_crypt = self.connections[player_name]['header_crypt']
    #             except KeyError:
    #                 # on login step player object not registered in self.connections,
    #                 # just ignore
    #                 pass
    #             else:
    #                 try:
    #                     response = WorldPacketManager.generate_packet(
    #                         opcode=WorldOpCode.SMSG_NAME_QUERY_RESPONSE,
    #                         data=name_query_packet,
    #                         header_crypt=header_crypt
    #                     )
    #                     writer.write(response)
    #                     await writer.drain()
    #                 except BrokenPipeError:
    #                     del self.connections[player_name]
    #
    #                 except ConnectionResetError:
    #                     del self.connections[player_name]
    #         finally:
    #             await asyncio.sleep(0.01)

    @staticmethod
    def create():
        Logger.info('[World Server]: init')
        return WorldServer(Config.Realm.Connection.WorldServer.host, Config.Realm.Connection.WorldServer.port)
