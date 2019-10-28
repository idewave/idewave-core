from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Connection.Connection import Connection


class InitialSpells(object):

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data', bytes())
        self.connection: Connection = kwargs.pop('connection')

    async def process(self) -> tuple:
        response = self._get_response()
        return WorldOpCode.SMSG_INITIAL_SPELLS, [response]

    def _get_response(self):
        data = bytes()

        num_spells = len(self.connection.player.spells)
        data += pack(
            '<BH',
            0,                  # unk
            num_spells          # spell count
        )

        count = 1
        for spell in self.connection.player.spells:
            data += pack(
                '<2H',
                spell.spell_template.entry,
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
        #         spell.entry,            # spell entry
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
