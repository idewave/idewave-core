from struct import pack
from typing import Optional

from Server.Connection.Connection import Connection

from World.Observer.WorldObserver import WorldObserver

from World.WorldPacket.Constants import LoginOpCode, WorldOpCode, ANY_OPCODE
from World.WorldPacket.Constants.OpcodeHandlerMap import OPCODE_HANDLER_MAP
from Utils.Debug import Logger


class WorldPacketManager(object):

    __slots__ = ('connection', 'world_observer')

    def __init__(self, **kwargs):
        self.connection: Connection = kwargs.pop('connection')
        self.world_observer: WorldObserver = kwargs.get('world_observer')

    async def process(self, **kwargs):
        size_bytes: bytes = kwargs.pop('size', None)
        opcode_bytes: bytes = kwargs.pop('opcode')
        data_bytes: bytes = kwargs.pop('data')

        if self.connection.header_crypt:
            decrypted_packet = self._decrypt(size_bytes + opcode_bytes + data_bytes)
            opcode_bytes = decrypted_packet[2:6]
            data_bytes = decrypted_packet[6:]

        opcode = WorldPacketManager._get_opcode_from_bytes(opcode_bytes)
        if opcode is None:
            return None

        if opcode in OPCODE_HANDLER_MAP:
            Logger.notify('[World Packet]: processing {} opcode'.format(opcode.name))
            handlers = OPCODE_HANDLER_MAP[opcode]
            packets = []

            for handler in handlers:
                opcode, response = await self._process_handler(handler, opcode, data_bytes)
                if opcode and response:
                    for data in response:
                        packet = self.generate_packet(opcode, data)
                        packets.append(packet)

            return packets
        else:
            Logger.warning('[World Packet]: no handler for opcode = {}'.format(opcode.name))
            return None

    async def _process_handler(self, handler, opcode: ANY_OPCODE, data: bytes):
        opcode, response = await handler(
            opcode=opcode,
            data=data,
            connection=self.connection,
            world_observer=self.world_observer
        ).process()

        return opcode, response

    @staticmethod
    def _get_opcode_from_bytes(opcode_bytes: bytes) -> Optional[ANY_OPCODE]:
        opcode = int.from_bytes(opcode_bytes, 'little')

        if len(opcode_bytes) == 1:
            return LoginOpCode.get_opcode(opcode)
        elif len(opcode_bytes) == 4:
            return WorldOpCode.get_opcode(opcode)
        else:
            return None

    def _decrypt(self, packet: bytes):
        # this is workaround cause one-time decryption do not works correctly for some opcodes
        # so I need decrypt some packets for multiple times
        result = packet
        for index in range(20):
            enc = self.connection.header_crypt.decrypt(packet)
            if WorldOpCode.has_value(int.from_bytes(enc[2:6], 'little')):
                result = enc
                break

        return result

    def generate_packet(self, opcode: ANY_OPCODE, data: bytes) -> bytes:
        Logger.success('[World Packet]: respond with {}'.format(opcode.name))

        if isinstance(opcode, LoginOpCode):
            return pack('<B', opcode.value) + data

        opcode_bytes = pack('<H', opcode.value)
        packet = opcode_bytes + data
        size_bytes = pack('>H', len(packet))
        packet = size_bytes + packet

        if self.connection.header_crypt:
            packet = self.connection.header_crypt.encrypt(packet)

        return packet
