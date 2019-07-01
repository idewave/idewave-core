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

    MAX_UPDATE_PACKETS_INCLUDED = 15

    def __init__(self, host, port):
        super().__init__(host, port)
        # key = player name, value = (reader, writer)
        self.connections = {}

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        temp_ref = TempRef()
        world_packet_manager = WorldPacketManager(temp_ref=temp_ref, reader=reader, writer=writer)

        peername = writer.get_extra_info('peername')
        Logger.debug('[World Server]: Accept connection from {}'.format(peername))

        Logger.info('[World Server]: trying to process auth session')
        auth = AuthManager(reader, writer, temp_ref=temp_ref, world_packet_manager=world_packet_manager)
        await auth.process(step=AuthStep.SECOND)

        while True:
            try:
                request = await asyncio.wait_for(reader.read(4096), timeout=1.0)
                if request:
                    response = await asyncio.wait_for(world_packet_manager.process(request), timeout=1.0)

                    if response:
                        for packet in response:
                            writer.write(packet)
                            await writer.drain()

            except TimeoutError:
                continue

            except Exception as e:
                Logger.error('[World Server]: exception, {}'.format(e))
                traceback.print_exc()
                break

            finally:
                await asyncio.sleep(1)

        writer.close()

    async def refresh_connections(self):
        while True:
            try:
                player_name, reader, writer, header_crypt = await asyncio.wait_for(
                    QueuesRegistry.connections_queue.get(), timeout=1.0
                )
            except TimeoutError:
                pass
            else:
                self.connections[player_name] = {
                    'reader': reader,
                    'writer': writer,
                    'header_crypt': header_crypt
                }
                Logger.info('[World Server]: new connection for player "{}"'.format(player_name))

    async def send_update_packet_to_player(self):
        while True:
            try:
                player_name, update_packets = await asyncio.wait_for(
                    QueuesRegistry.update_packets_queue.get(),
                    timeout=1.0
                )
            except TimeoutError:
                pass
            else:
                try:
                    writer = self.connections[player_name]['writer']
                    header_crypt = self.connections[player_name]['header_crypt']
                except KeyError:
                    # do nothing for this because on login step player not saved in self.connections
                    pass
                else:

                    responses = []

                    while update_packets:
                        # batches with chained with this packet
                        head_update_packet_builder = update_packets.pop(0)

                        for index in range(0, WorldServer.MAX_UPDATE_PACKETS_INCLUDED):

                            if not update_packets:
                                break

                            batch = update_packets.pop(0).get_update_packet()
                            head_update_packet_builder.add_batch(batch)

                        update_packet = head_update_packet_builder.get_update_packet(build=True)

                        responses.append(update_packet)

                    for update_packet in responses:
                        response = WorldPacketManager.generate_packet(
                            opcode=WorldOpCode.SMSG_UPDATE_OBJECT,
                            data=update_packet,
                            header_crypt=header_crypt
                        )
                        writer.write(response)
                        await writer.drain()

                finally:
                    await asyncio.sleep(1)

    @staticmethod
    def create():
        Logger.info('[World Server]: init')
        return WorldServer(Config.Realm.Connection.WorldServer.host, Config.Realm.Connection.WorldServer.port)
