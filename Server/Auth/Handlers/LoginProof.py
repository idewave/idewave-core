from base64 import b64encode
from struct import unpack, pack

from World.WorldPacket.Constants.LoginOpCode import LoginOpCode
from Server.Auth.Constants.LoginResult import LoginResult
from Server.Registry.QueuesRegistry import QueuesRegistry

from Server.Connection.Connection import Connection

from Exceptions.Wrappers.ProcessException import ProcessException


class LoginProof(object):

    LOGIN_PROOF_FORMAT = '<32s20s20sBx'

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data')

        self.client_ephemeral = 0
        self.client_proof = bytes()
        self.checksum = bytes()
        self.unk = 0

        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        self._parse_data()

        self.connection.srp.generate_session_key(self.client_ephemeral, self.connection.account.verifier)
        self.connection.srp.generate_client_proof(self.client_ephemeral, self.connection.account)

        response = None

        if self.connection.srp.client_proof == self.client_proof:
            self.connection.srp.generate_server_proof(self.client_ephemeral)

            await QueuesRegistry.session_keys_queue.put((
                '#{}-session-key'.format(self.connection.account.name),
                b64encode(self.connection.srp.session_key).decode('utf-8')
            ))

            response = pack(
                '<B20sQ2B',
                LoginResult.SUCCESS.value,
                self.connection.srp.server_proof,
                0x00800000,
                0x00,
                0x00
            )

        return LoginOpCode.LOGIN_PROOF, [response]

    @ProcessException
    def _parse_data(self):
        parsed_data = unpack(LoginProof.LOGIN_PROOF_FORMAT, self.data)
        self.client_ephemeral = int.from_bytes(parsed_data[0], 'little')
        self.client_proof = parsed_data[1]
        self.checksum = parsed_data[2]
        self.unk = parsed_data[3]
