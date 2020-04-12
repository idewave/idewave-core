import asyncio

from asyncio.streams import StreamReader, StreamWriter
from asyncio import TimeoutError

from Server import BaseServer, Connection
from World.WorldPacket.WorldPacketManager import WorldPacketManager
from Utils.Debug import Logger


class LoginServer(BaseServer):

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        peername = writer.get_extra_info('peername')
        Logger.info('[Login Server]: Accepted connection from {}'.format(peername))

        connection = Connection(reader=reader, writer=writer, peername=peername)
        world_packet_mgr = WorldPacketManager(connection=connection)

        while True:
            try:
                await LoginServer.process_request(reader, writer, world_packet_mgr)
            except TimeoutError:
                continue
            finally:
                await asyncio.sleep(LoginServer.from_config('server:settings:min_timeout'))

    @staticmethod
    async def process_request(
            reader: StreamReader,
            writer: StreamWriter,
            world_packet_mgr: WorldPacketManager
    ):
        request = await asyncio.wait_for(
            reader.read(4096),
            timeout=LoginServer.from_config('server:settings:min_timeout')
        )
        if request:
            opcode, data = request[:1], request[1:]

            if data:
                response = await asyncio.wait_for(
                    world_packet_mgr.process(opcode=opcode, data=data),
                    timeout=LoginServer.from_config('server:settings:min_timeout')
                )

                if response:
                    for packet in response:
                        writer.write(packet)
                        await writer.drain()

    @staticmethod
    def create():
        Logger.info('[Login Server]: init')

        return LoginServer(
            host=LoginServer.from_config('server:connection:login_server:host'),
            port=LoginServer.from_config('server:connection:login_server:port')
        )
