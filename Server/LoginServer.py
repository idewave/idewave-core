from asyncio.streams import StreamReader, StreamWriter

from Utils.TempRef import TempRef
from Server.BaseServer import BaseServer
from Auth.AuthManager import AuthManager
from Auth.Constants.AuthStep import AuthStep
from Utils.Debug.Logger import Logger
from Config.Run.config import Config


class LoginServer(BaseServer):

    def __init__(self, host, port):
        super().__init__(host, port)

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        peername = writer.get_extra_info('peername')
        Logger.info('[Login Server]: Accepted connection from {}'.format(peername))

        temp_ref = TempRef()

        auth = AuthManager(reader, writer, temp_ref=temp_ref)
        await auth.process(step=AuthStep.FIRST)
        writer.close()

    @staticmethod
    def create():
        Logger.info('[Login Server]: init')
        return LoginServer(Config.Realm.Connection.LoginServer.host, Config.Realm.Connection.LoginServer.port)
