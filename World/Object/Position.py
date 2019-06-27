from struct import pack


class Position(object):

    def __init__(self, **kwargs):
        self.x = kwargs.pop('x', float(0))
        self.y = kwargs.pop('y', float(0))
        self.z = kwargs.pop('z', float(0))
        self.orientation = kwargs.pop('orientation', float(0))
        self.region_id = kwargs.pop('region_id', None)
        self.map_id = kwargs.pop('map_id', None)

    def to_bytes(self):
        return pack('<4f', self.x, self.y, self.z, self.orientation)

    def to_json(self):
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'orientation': self.orientation
        }
