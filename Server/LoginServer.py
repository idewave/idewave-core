import asyncio

from asyncio.streams import StreamReader, StreamWriter
from asyncio import TimeoutError

from Server.BaseServer import BaseServer
from Server.Connection.Connection import Connection
from World.WorldPacket.WorldPacketManager import WorldPacketManager
from Utils.Debug.Logger import Logger
from Config.Run.config import Config

from Server.Constants.ServerContants import MIN_TIMEOUT


class LoginServer(BaseServer):

    def __init__(self, host, port):
        super().__init__(host, port)

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
                await asyncio.sleep(MIN_TIMEOUT)

    @staticmethod
    async def process_request(reader: StreamReader, writer: StreamWriter, world_packet_mgr: WorldPacketManager):
        request = await asyncio.wait_for(reader.read(4096), timeout=MIN_TIMEOUT)
        if request:
            opcode, data = request[:1], request[1:]

            if data:
                response = await asyncio.wait_for(
                    world_packet_mgr.process(opcode=opcode, data=data),
                    timeout=MIN_TIMEOUT
                )

                if response:
                    for packet in response:
                        writer.write(packet)
                        await writer.drain()

    @staticmethod
    def create():
        Logger.info('[Login Server]: init')
        return LoginServer(Config.Realm.Connection.LoginServer.host, Config.Realm.Connection.LoginServer.port)
