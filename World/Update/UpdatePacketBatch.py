from World.Update.UpdatePacket import UpdatePacket
from struct import pack
from Utils.Debug.Logger import Logger


class UpdatePacketBatch(object):

    def __init__(self):
        self.packet = bytes()
        # total amount of update entities
        self.count = 0
        self.has_transport = int(False)

    def add_packet(self, batch: UpdatePacket):
        self.packet += batch
        self.count += 1

    def get_packet(self, build=False):
        if build:
            header = pack(
                '<IB',
                self.count,
                self.has_transport
            )
            return header + self.packet
        else:
            return self.packet
