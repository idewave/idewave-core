import asyncio
import traceback

from asyncio.streams import StreamReader, StreamWriter
from concurrent.futures import TimeoutError

from Utils.TempRef import TempRef
from Server.BaseServer import BaseServer
from Utils.Debug.Logger import Logger
from Auth.AuthManager import AuthManager
from Auth.Constants.AuthStep import AuthStep
from Server.Registry.QueuesRegistry import QueuesRegistry
from World.WorldPacket.WorldPacketManager import WorldPacketManager
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode

from Config.Run.config import Config


class WorldServer(BaseServer):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.session_keys = {}
        # key = player name, value = (reader, writer)
        self.connections = {}

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        self._register_tasks()

        temp_ref = TempRef()
        world_packet_manager = WorldPacketManager(temp_ref=temp_ref, reader=reader, writer=writer)

        Logger.info('[World Server]: trying to process auth session')
        auth = AuthManager(
            reader,
            writer,
            temp_ref=temp_ref,
            world_packet_manager=world_packet_manager,
            session_keys=self.session_keys
        )

        is_authenticated = await auth.process(step=AuthStep.SECOND)

        if is_authenticated:

            peer_name = writer.get_extra_info('peername')
            Logger.success('[World Server]: Accept connection from {}'.format(peer_name))

            while True:
                try:
                    request = await asyncio.wait_for(reader.read(4096), timeout=0.01)
                    if request:
                        response = await asyncio.wait_for(world_packet_manager.process(request), timeout=0.01)

                        if response:
                            for packet in response:
                                writer.write(packet)
                                await writer.drain()

                except TimeoutError:
                    pass

                except BrokenPipeError:
                    pass

                except Exception as e:
                    Logger.error('[World Server]: exception, {}'.format(e))
                    traceback.print_exc()
                    break
                finally:
                    await asyncio.sleep(0.01)

        writer.close()

    def _register_tasks(self):
        asyncio.gather(
            asyncio.ensure_future(self.add_connection()),
            asyncio.ensure_future(self.remove_connection()),
            asyncio.ensure_future(self.add_session_keys()),
            asyncio.ensure_future(self.send_update_packet_to_player()),
            asyncio.ensure_future(self.send_movement_packet_to_player()),
            asyncio.ensure_future(self.send_text_message_packet_to_player()),
            asyncio.ensure_future(self.send_name_query_packet_to_player()),
        )

    async def add_connection(self):
        while True:
            try:
                player_name, reader, writer, header_crypt = QueuesRegistry.connections_queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            else:
                self.connections[player_name] = {
                    'reader': reader,
                    'writer': writer,
                    'header_crypt': header_crypt
                }
                Logger.info('[World Server]: added connection for player "{}"'.format(player_name))
            finally:
                await asyncio.sleep(0.01)

    async def remove_connection(self):
        while True:
            try:
                player_name = QueuesRegistry.disconnect_queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            else:
                if player_name and self.connections and player_name in self.connections:
                    del self.connections[player_name]
                    Logger.info('[World Server]: player "{}" disconnected'.format(player_name))
            finally:
                await asyncio.sleep(0.01)

    async def add_session_keys(self):
        while True:
            try:
                key, value = QueuesRegistry.session_keys_queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            else:
                self.session_keys[key] = value
            finally:
                await asyncio.sleep(0.01)

    async def send_update_packet_to_player(self):
        while True:
            try:
                player_name, update_packets = await asyncio.wait_for(
                    QueuesRegistry.update_packets_queue.get(),
                    timeout=0.01
                )
            except TimeoutError:
                pass
            else:
                try:
                    writer = self.connections[player_name]['writer']
                    header_crypt = self.connections[player_name]['header_crypt']
                except KeyError:
                    # on login step player object not registered in self.connections,
                    # just ignore
                    pass
                else:
                    try:
                        for update_packet in update_packets:
                            response = WorldPacketManager.generate_packet(
                                opcode=WorldOpCode.SMSG_UPDATE_OBJECT,
                                data=update_packet,
                                header_crypt=header_crypt
                            )
                            Logger.test('Send update packet to {}'.format(player_name))
                            writer.write(response)
                            await writer.drain()
                    except BrokenPipeError:
                        del self.connections[player_name]

                    except ConnectionResetError:
                        del self.connections[player_name]
            finally:
                await asyncio.sleep(0.01)

    async def send_movement_packet_to_player(self):
        while True:
            try:
                player_name, movement_packet, opcode = await asyncio.wait_for(
                    QueuesRegistry.movement_packets_queue.get(),
                    timeout=0.01
                )
                # player_name, movement_packet, opcode = QueuesRegistry.movement_packets_queue.get_nowait()
            # except asyncio.QueueEmpty:
            #     pass
            except TimeoutError:
                pass
            else:
                try:
                    writer = self.connections[player_name]['writer']
                    header_crypt = self.connections[player_name]['header_crypt']
                except KeyError:
                    # on login step player object not registered in self.connections,
                    # just ignore
                    pass
                else:
                    try:
                        response = WorldPacketManager.generate_packet(
                            opcode=opcode,
                            data=movement_packet,
                            header_crypt=header_crypt
                        )
                        writer.write(response)
                        await writer.drain()
                    except BrokenPipeError:
                        del self.connections[player_name]

                    except ConnectionResetError:
                        del self.connections[player_name]
            finally:
                await asyncio.sleep(0.01)

    async def send_text_message_packet_to_player(self):
        while True:
            try:
                player_name, text_message_packet = await asyncio.wait_for(
                    QueuesRegistry.text_message_packets_queue.get(),
                    timeout=0.01
                )
            # except asyncio.QueueEmpty:
            #     pass
            except TimeoutError:
                pass
            else:
                try:
                    writer = self.connections[player_name]['writer']
                    header_crypt = self.connections[player_name]['header_crypt']
                except KeyError:
                    # on login step player object not registered in self.connections,
                    # just ignore
                    pass
                else:
                    try:
                        response = WorldPacketManager.generate_packet(
                            opcode=WorldOpCode.SMSG_MESSAGECHAT,
                            data=text_message_packet,
                            header_crypt=header_crypt
                        )
                        writer.write(response)
                        await writer.drain()
                    except BrokenPipeError:
                        del self.connections[player_name]

                    except ConnectionResetError:
                        del self.connections[player_name]
            finally:
                await asyncio.sleep(0.01)

    async def send_name_query_packet_to_player(self):
        while True:
            try:
                player_name, name_query_packet = await asyncio.wait_for(
                    QueuesRegistry.name_query_packets_queue.get(),
                    timeout=0.01
                )
            # except asyncio.QueueEmpty:
            #     pass
            except TimeoutError:
                pass
            else:
                try:
                    writer = self.connections[player_name]['writer']
                    header_crypt = self.connections[player_name]['header_crypt']
                except KeyError:
                    # on login step player object not registered in self.connections,
                    # just ignore
                    pass
                else:
                    try:
                        response = WorldPacketManager.generate_packet(
                            opcode=WorldOpCode.SMSG_NAME_QUERY_RESPONSE,
                            data=name_query_packet,
                            header_crypt=header_crypt
                        )
                        writer.write(response)
                        await writer.drain()
                    except BrokenPipeError:
                        del self.connections[player_name]

                    except ConnectionResetError:
                        del self.connections[player_name]
            finally:
                await asyncio.sleep(0.01)

    @staticmethod
    def create():
        Logger.info('[World Server]: init')
        return WorldServer(Config.Realm.Connection.WorldServer.host, Config.Realm.Connection.WorldServer.port)
