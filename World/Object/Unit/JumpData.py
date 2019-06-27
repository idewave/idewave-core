from struct import pack


class JumpData(object):

    def __init__(self):
        self.time = 0
        self.velocity = float(0)
        self.sin = float(0)
        self.cos = float(0)
        self.xy_speed = float(0)

    def to_bytes(self):
        return pack(
            '<I4f',
            self.time,
            self.velocity,
            self.sin,
            self.cos,
            self.xy_speed
        )
