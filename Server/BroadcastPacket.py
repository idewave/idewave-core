from Server import Packet


class BroadcastPacket(Packet):

    def __init__(self):
        super().__init__()
        self.broadcast_range: int = 0
