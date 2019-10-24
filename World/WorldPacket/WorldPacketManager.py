from struct import pack
from typing import Union

from Server.Connection.Connection import Connection

from World.WorldPacket.Constants.LoginOpCode import LoginOpCode
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.WorldPacket.Constants.MapHandlerToOpcode import MAP_HANDLER_TO_OPCODE
from Utils.Debug.Logger import Logger

from Exceptions.Wrappers.ProcessException import ProcessException


class WorldPacketManager(object):

    __slots__ = ('connection',)

    def __init__(self, **kwargs):
        self.connection: Connection = kwargs.pop('connection')

    async def process(self, **kwargs):
        size = kwargs.pop('size', None)
        opcode = kwargs.pop('opcode')
        data = kwargs.pop('data')

        if not bool(opcode) or not bool(data):
            return None

        if self.connection.header_crypt:
            packet = self._decrypt(size + opcode + data)
            opcode = packet[2:6]
            data = packet[6:]

        opcode: Union[LoginOpCode, WorldOpCode, None] = WorldPacketManager._get_opcode_from_bytes(opcode)
        if opcode is None:
            return None

        if opcode in MAP_HANDLER_TO_OPCODE:
            Logger.notify('[World Packet]: processing {} opcode'.format(opcode.name))
            handlers = MAP_HANDLER_TO_OPCODE[opcode]
            packets = []

            for handler in handlers:
                opcode, response = await self._process_handler(handler, opcode, data)
                if opcode and response:
                    for data in response:
                        packets.append(self.generate_packet(opcode, data))

            return packets
        else:
            Logger.warning('[World Packet]: no handler for opcode = {}'.format(opcode.name))

    @ProcessException
    async def _process_handler(self, handler, opcode: Union[LoginOpCode, WorldOpCode], data: bytes):
        opcode, response = await handler(opcode=opcode, data=data, connection=self.connection).process()
        return opcode, response

    @staticmethod
    def _get_opcode_from_bytes(opcode: bytes):
        opcode = int.from_bytes(opcode, 'little')
        return LoginOpCode.get_opcode(opcode) or WorldOpCode.get_opcode(opcode) or None

    @ProcessException
    def _decrypt(self, packet: bytes):
        # this is workaround cause one-time decryption do not works correctly for some opcodes
        # so I need decrypt some packets for multiple times
        result = packet
        for index in range(20):
            enc = self.connection.header_crypt.decrypt(packet)
            if WorldOpCode.get_opcode(int.from_bytes(enc[2:6], 'little')):
                result = enc
                break

        return result

    @ProcessException
    def generate_packet(self, opcode: Union[LoginOpCode, WorldOpCode], data: bytes):
        Logger.success('[World Packet]: respond with {}'.format(opcode.name))

        if isinstance(opcode, LoginOpCode):
            return pack('<B', opcode.value) + data

        opcode_bytes = pack('<H', opcode.value)
        packet = opcode_bytes + data
        size_bytes = pack('>H', len(packet))
        packet = size_bytes + packet

        if self.connection.header_crypt is not None:
            packet = self.connection.header_crypt.encrypt(packet)

        return packet
