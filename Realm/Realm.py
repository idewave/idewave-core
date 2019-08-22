from struct import pack

from Realm.Constants.RealmTimeZone import RealmTimezone


class Realm(object):

    REALM_PACKET_FORMAT = '<2B{name_len}s{addr_len}sf4B'

    def __init__(self, name, host, port, type):
        self.name = name
        self.address = host + ':' + str(port)
        self.type = type

    def get_state_packet(self, flags, population):
        name_bytes = self.name.encode('ascii') + b'\x00'
        address_bytes = self.address.encode('ascii') + b'\x00'
        # TODO: get chars number for current account from REALM DB
        num_chars = 1

        packet = pack(
            Realm.REALM_PACKET_FORMAT.format(name_len=len(name_bytes), addr_len=len(address_bytes)),
            self.type,
            flags,
            name_bytes,
            address_bytes,
            population,
            num_chars,
            RealmTimezone.DEVELOPMENT.value,
            0x2c,   # unknown
            0x0010  # ?
        )

        size_bytes = int.to_bytes(len(packet), 1, 'little')
        return size_bytes + packet
