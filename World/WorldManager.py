from asyncio import QueueEmpty, ensure_future, sleep, gather

from Utils.Timer import Timer
from World.Region.RegionManager import RegionManager
from World.Region.Weather.WeatherManager import WeatherManager
from Server.Registry.QueuesRegistry import QueuesRegistry
from Config.Mixins import ConfigurableMixin


class WorldManager(ConfigurableMixin):

    __slots__ = ('last_update', 'region_mgr', 'weather_mgr')

    def __init__(self):
        self.last_update = None
        self.region_mgr = RegionManager()
        self.weather_mgr = WeatherManager(
            instant_change=WorldManager.from_config('region:weather:instant_change')
        )

    async def run(self):
        self._register_tasks()

        while True:
            self.last_update = Timer.get_ms_time()
            await sleep(WorldManager.from_config('server:settings:min_timeout'))

    def _register_tasks(self):
        gather(
            ensure_future(self.process_broadcast()),
            ensure_future(self.change_weather()),
        )

    async def process_broadcast(self):
        while True:
            try:
                # notice: second parameter (packets) should be list, not string
                opcode, packets, callback = QueuesRegistry.broadcast_callback_queue.get_nowait()
            except QueueEmpty:
                pass
            else:
                self.region_mgr.broadcast(opcode, packets, callback)
            finally:
                await sleep(WorldManager.from_config('server:settings:min_timeout'))

    async def change_weather(self):
        while True:
            self.weather_mgr.set_weather()
            await sleep(WorldManager.from_config('region:weather:change_weather_timeout'))
