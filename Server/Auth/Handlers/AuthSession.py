from struct import pack

from Server.Connection.Connection import Connection
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Auth.Constants.ResponseCodes import ResponseCodes


class AuthSession(object):

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data')
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        response = pack(
            '<BIBIB',
            ResponseCodes.AUTH_OK.value,
            0x00,                           # BillingTimeRemaining
            0x00,                           # BillingPlanFlags
            0x00,                           # BillingTimeRested
            0x01                            # Expansion, 0 - normal, 1 - TBC, must be set manually for each account
        )
        return WorldOpCode.SMSG_AUTH_RESPONSE, [response]
