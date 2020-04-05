from typing import Optional

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class Packet(object):

    def __init__(self):
        self.opcode: Optional[WorldOpCode] = None
        self.body: bytes = bytes()
