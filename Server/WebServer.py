import json
from aiohttp import web
from Utils.Debug.Logger import Logger
from Server.Registry.QueuesRegistry import QueuesRegistry
from Config.Run.config import Config


class WebServer(object):

    @staticmethod
    async def websocket_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            d = await QueuesRegistry.web_data_queue.get_object_field()
            data = json.loads(msg.data)
            if data['type'] == 'REQUEST_POSITION':
                ws.send_str(str(d))

        return ws

    @staticmethod
    def run():
        Logger.info('[Web Server]: init')
        app = web.Application()
        app.router.add_routes([
            web.get('/', WebServer.websocket_handler)
        ])
        web.run_app(app, host=Config.WebServer.Connection.host, port=Config.WebServer.Connection.port)
