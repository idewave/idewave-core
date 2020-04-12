from asyncio import ensure_future
from typing import Dict, List
from random import uniform, choice, randint
from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.Region.model import Region
from World.Region.Weather.Constants.WeatherType import WeatherType
from World.Object.Unit.Player.model import Player
from World.Object.Unit.Player.PlayerManager import PlayerManager
from World.Region.Octree.OctreeNodeManager import OctreeNodeManager
from World.Region.Octree.Node import ChildNode
from Server.Registry.QueuesRegistry import QueuesRegistry
from Config.Mixins import ConfigurableMixin


class WeatherManager(ConfigurableMixin):

    __slots__ = ('weather_types', 'current_weather_type', 'instant_change')

    def __init__(self, **kwargs):
        self.current_weather_type: int = 0
        self.weather_types: List[WeatherType] = [item for item in WeatherType]
        self.instant_change: bool = kwargs.pop('instant_change')

    def set_weather(self) -> None:
        self._change_state()

        ensure_future(QueuesRegistry.broadcast_callback_queue.put((
            WorldOpCode.SMSG_WEATHER,
            [self._create_weather_packet()],
            WeatherManager.broadcast,
        )))

    def _change_state(self) -> None:
        chance_to_change = randint(1, 100)
        chances: Dict[str, int] = WeatherManager.from_config('region:weather:change_chance')

        allowed_weather_types: List[int] = [
            wtype.value
            for wtype in self.weather_types
            if getattr(chances, wtype.name.lower()) >= chance_to_change
        ]

        if allowed_weather_types:
            self.current_weather_type = choice(allowed_weather_types)

    def _create_weather_packet(self) -> bytes:
        response = pack(
            '<IfB',
            self.current_weather_type,
            uniform(0, 1),                  # intensity
            int(self.instant_change)        # 0 - smooth change, 1 - instant change
        )
        return response

    @staticmethod
    def broadcast(**kwargs) -> None:
        opcode: WorldOpCode = kwargs.pop('opcode')
        packets: List[bytes] = kwargs.pop('packets')
        regions: Dict[int, Region] = kwargs.pop('regions')

        for region in regions.values():
            root_node: ChildNode = region.get_octree()
            guids = OctreeNodeManager.get_guids(root_node)

            if not guids:
                continue

            targets_to_notify: List[Player] = [
                player
                for player in region.players
                if player.guid in guids
            ]

            if not targets_to_notify:
                continue

            for packet in packets:
                PlayerManager.broadcast(opcode, packet, targets_to_notify)
