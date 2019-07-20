import asyncio
import websockets
import json

from websockets.exceptions import ConnectionClosedOK
from websockets import WebSocketCommonProtocol
from asyncio.futures import TimeoutError

from Server.Registry.QueuesRegistry import QueuesRegistry
from Server.WebsocketServer.Constants.RequestType import RequestType

from Utils.Debug.Logger import Logger
from Config.Run.config import Config


class WebsocketServer(object):

    def __init__(self, host, port):
        self.instance = websockets.serve(self.handle_connection, host, port)
        self.connections = []
        self.web_data = None

    def get_instance(self):
        return self.instance

    async def get_web_data(self):
        while True:
            try:
                self.web_data = await asyncio.wait_for(QueuesRegistry.web_data_queue.get(), timeout=0.5)
            except TimeoutError:
                continue

    async def accept_connection(self, websocket: WebSocketCommonProtocol):
        while True:
            try:
                request = await asyncio.wait_for(websocket.recv(), timeout=1.0)
            except TimeoutError:
                continue
            else:
                parsed_request = json.loads(request)
                if 'type' in parsed_request and parsed_request['type'] == RequestType.SUBSCRIBE.value:
                    Logger.success('[Websocket Server]: new connection was added, {}'.format(websocket.local_address))
                    self.connections.append(websocket)

    async def handle_connection(self, websocket: WebSocketCommonProtocol, path):
        asyncio.create_task(self.accept_connection(websocket))

        while True:
            try:
                await websocket.send(json.dumps(self.web_data))
            except ConnectionClosedOK:
                Logger.error('[Websocket Server]: Connection was closed')
                return
            except Exception as e:
                Logger.error('[Websocket Server]: {}'.format(type(e)))
                continue

    @staticmethod
    def create():
        Logger.info('[Websocket Server]: init')
        return WebsocketServer(
            Config.WebsocketServer.Connection.host,
            Config.WebsocketServer.Connection.port
        )
