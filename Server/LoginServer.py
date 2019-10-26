import asyncio

from asyncio.streams import StreamReader, StreamWriter

from Server.BaseServer import BaseServer
from Server.Connection.Connection import Connection
from World.WorldPacket.WorldPacketManager import WorldPacketManager
from Utils.Debug.Logger import Logger
from Config.Run.config import Config

from Exceptions.Wrappers.ProcessException import ProcessException


class LoginServer(BaseServer):

    def __init__(self, host, port):
        super().__init__(host, port)

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        peername = writer.get_extra_info('peername')
        Logger.info('[Login Server]: Accepted connection from {}'.format(peername))

        connection = Connection(reader=reader, writer=writer, peername=peername)
        world_packet_mgr = WorldPacketManager(connection=connection)

        while True:
            await self._process_request(reader, writer, world_packet_mgr)

    @ProcessException
    async def _process_request(self, reader: StreamReader, writer: StreamWriter, world_packet_mgr: WorldPacketManager):
        request = await asyncio.wait_for(reader.read(4096), timeout=0.01)
        if request:
            opcode, data = request[:1], request[1:]

            if data:
                response = await asyncio.wait_for(world_packet_mgr.process(opcode=opcode, data=data), timeout=0.01)

                if response:
                    for packet in response:
                        writer.write(packet)
                        await writer.drain()

        await asyncio.sleep(0.01)

    @staticmethod
    def create():
        Logger.info('[Login Server]: init')
        return LoginServer(Config.Realm.Connection.LoginServer.host, Config.Realm.Connection.LoginServer.port)
