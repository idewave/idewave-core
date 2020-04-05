from struct import pack
from typing import Optional, Dict


class Position(object):

    def __init__(self, **kwargs):
        self.x: float = kwargs.pop('x', float(0))
        self.y: float = kwargs.pop('y', float(0))
        self.z: float = kwargs.pop('z', float(0))
        self.orientation: float = kwargs.pop('orientation', float(0))

        self.region_id: Optional[int] = kwargs.pop('region_id', None)
        self.map_id: Optional[int] = kwargs.pop('map_id', None)

    def to_bytes(self) -> bytes:
        return pack(
            '<4f',
            self.x,
            self.y,
            self.z,
            self.orientation
        )

    def to_json(self) -> Dict[str, float]:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'orientation': self.orientation
        }
