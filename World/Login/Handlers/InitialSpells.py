from struct import pack

from World.WorldPacket.Constants.WorldOpCode import WorldOpCode


class InitialSpells(object):

    def __init__(self, packet: bytes, **kwargs):
        self.packet = packet
        self.temp_ref = kwargs.pop('temp_ref', None)
        if self.temp_ref is None:
            raise Exception('[Initial Spells]: temp_ref does not exists')

        self.player = self.temp_ref.player

    async def process(self):
        response = self._get_response()
        return WorldOpCode.SMSG_INITIAL_SPELLS, response

    def _get_response(self):
        data = bytes()

        num_spells = len(self.player.spells)
        data += pack(
            '<BH',
            0,                  # unk
            num_spells          # spell count
        )

        count = 1
        for spell in self.player.spells:
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
