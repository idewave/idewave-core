from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from struct import pack
from Login.SessionStorage import session


class InitialSpells(object):

    def __init__(self, packet: bytes):
        self.packet = packet

    async def process(self):
        data = self._prepare()
        #data = b'\x00$\x00\x0bV\x00\x00\x93T\x00\x00\x11R\x00\x00iP\x00\x00gP\x00\x00dP\x00\x00\xa5#\x00\x00v#\x00\x00\xc2 \x00\x00I\x02\x00\x00Q\x00\x00\x00\x9f\x02\x00\x00\x9c\x02\x00\x00\xc6\x00\x00\x00fP\x00\x00g\x18\x00\x00M\x19\x00\x00\n\x02\x00\x00\x1aY\x00\x00\xcb\x00\x00\x00\x94T\x00\x00N\t\x00\x00\xea\x0b\x00\x00f\x18\x00\x00\xcc\x00\x00\x00\xaf\t\x00\x00\x91\x13\x00\x00\x9b\x13\x00\x00c\x1c\x00\x00\x02\x08\x00\x00Y\x18\x00\x00N\x19\x00\x00\xbb\x1c\x00\x00\xcb\x19\x00\x00%\r\x00\x00b\x1c\x00\x00\x00\x00'
        return WorldOpCode.SMSG_INITIAL_SPELLS, data

    def _prepare(self):
        data = bytes()

        num_spells = len(session.player.spells)
        data += pack(
            '<BH',
            0,                  # unk
            num_spells          # spell count
        )

        count = 1
        for spell in session.player.spells:
            data += pack(
                '<2H',
                spell.id,
                0
            )
            count += 1

        data += pack(
            '<2H',
            num_spells,
            0
        )

        # now = int(time.time())
        #
        # for spell in session.player.spells:
        #     values = 0
        #     data += pack(
        #         '<3H2I',
        #         spell.id,               # spell id
        #         0,                      # spell category
        #         0,                      # item id
        #         now,                    # cooldown
        #         0 | 0x80000000          # cooldown category
        #     )

        # data += pack(
        #     '<2H',
        #     0,
        #     0
        # )

        return data
