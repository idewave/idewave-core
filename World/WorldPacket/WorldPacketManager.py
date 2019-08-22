import traceback
from struct import pack, unpack

from Auth.Crypto.HeaderCrypt import HeaderCrypt

from Server.Exceptions.PlayerNotExists import PlayerNotExists

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from World.WorldPacket.Constants.MapHandlerToOpcode import MAP_HANDLER_TO_OPCODE
from Utils.Debug.Logger import Logger


class WorldPacketManager(object):

    def __init__(self, **kwargs):
        self.header_crypt = None
        self.temp_ref = kwargs.pop('temp_ref', None)

        self.reader = kwargs.pop('reader', None)
        self.writer = kwargs.pop('writer', None)

    async def process(self, packet: bytes):
        if not self.header_crypt:
            raise Exception('Cannot decrypt packet')

        # this is workaround cause one-time decryption do not works correctly for some opcodes
        # so I need decrypt some packets for multiple times
        def decrypt(packet: bytes):
            result = packet
            for index in range(20):
                enc = self.header_crypt.decrypt(packet)
                try:
                    # TODO: add has_key for Enum
                    WorldOpCode(int.from_bytes(enc[2:6], 'little')).value
                except ValueError:
                    continue
                else:
                    result = enc
                    break

            return result

        packet = decrypt(packet)

        size = unpack('>H', packet[:2])[0]
        opcode = WorldOpCode(unpack('<I', packet[2:6])[0])

        if opcode in MAP_HANDLER_TO_OPCODE:
            Logger.debug('[World Packet]: processing {} opcode ({} bytes)'.format(WorldOpCode(opcode).name, size))
            handlers = MAP_HANDLER_TO_OPCODE[opcode]
            packets = []

            for handler in handlers:
                try:
                    opcode, response = await handler(
                        packet,
                        temp_ref=self.temp_ref,
                        reader=self.reader,
                        writer=self.writer,
                        header_crypt=self.header_crypt
                    ).process()
                except PlayerNotExists:
                    self.writer.close()
                    return None
                except Exception as e:
                    Logger.error('[WorldPacketMgr]: !{}! {}'.format(handler, e))
                    traceback.print_exc()
                else:
                    if opcode and response:
                        if isinstance(response, list):
                            for packet in response:
                                packets.append(WorldPacketManager.generate_packet(opcode, packet, self.header_crypt))

                        else:
                            packets.append(WorldPacketManager.generate_packet(opcode, response, self.header_crypt))

            return packets
        else:
            try:
                Logger.warning(
                    '[World Packet]: no handler for opcode = {} ({} bytes)'.format(
                        WorldOpCode(opcode).name, size
                    ))
            except ValueError:
                Logger.error(
                    '[World Packet]: no handler for unknown opcode = {} ({} bytes)'.format(
                        opcode, size
                    ))
            finally:
                return None

    def set_header_crypt(self, header_crypt: HeaderCrypt):
        self.header_crypt = header_crypt

    @staticmethod
    def generate_packet(opcode: WorldOpCode, data: bytes, header_crypt: HeaderCrypt = None):
        opcode_bytes = pack('<H', opcode.value)
        packet = opcode_bytes + data
        size_bytes = pack('>H', len(packet))
        packet = size_bytes + packet

        if header_crypt is not None:
            packet = header_crypt.encrypt(packet)

        return packet
