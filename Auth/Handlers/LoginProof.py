from base64 import b64encode
from struct import unpack, pack, error as StructError

from Auth.Constants.LoginOpCode import LoginOpCode
from Auth.Constants.LoginResult import LoginResult
from Server.Registry.QueuesRegistry import QueuesRegistry
from Utils.Debug.Logger import Logger


class LoginProof(object):

    LOGIN_PROOF_FORMAT = '<32s20s20sBx'

    def __init__(self, **kwargs):
        self.packet = kwargs.pop('packet', bytes())
        self.client_ephemeral = 0
        self.client_proof = bytes()
        self.checksum = bytes()
        self.unk = 0

        self.srp = kwargs.pop('srp')

        temp_ref = kwargs.pop('temp_ref')
        if temp_ref is None:
            raise Exception('[LoginProof]: Something gone wrong in previous step')

        self.account = temp_ref.account

    async def process(self):
        Logger.debug('[Login Proof]: processing...')
        self._parse_data()

        # generated for server-side authentication (next step, after realmlist recv)
        self.srp.generate_session_key(self.client_ephemeral, self.account.verifier)
        self.srp.generate_client_proof(self.client_ephemeral, self.account)

        if self.srp.client_proof == self.client_proof:
            Logger.debug('[Login Proof]: OK')
            self.srp.generate_server_proof(self.client_ephemeral)

            await QueuesRegistry.session_keys_queue.put((
                '#{}-session-key'.format(self.account.name),
                b64encode(self.srp.session_key).decode('utf-8')
            ))

            return self._get_response()

        return None

    def _parse_data(self):
        try:
            parsed_data = unpack(LoginProof.LOGIN_PROOF_FORMAT, self.packet)
            self.client_ephemeral = int.from_bytes(parsed_data[0], 'little')
            self.client_proof = parsed_data[1]
            self.checksum = parsed_data[2]
            self.unk = parsed_data[3]
        except StructError as e:
            Logger.error('[Login Proof]: on unpacking data(len={}), error={}'.format(len(self.packet), e))

    def _get_response(self):
        try:
            response = pack(
                '<2B20sQ2B',
                LoginOpCode.LOGIN_PROOF.value,
                LoginResult.SUCCESS.value,
                self.srp.server_proof,
                0x00800000,
                0x00,
                0x00
            )
        except Exception as e:
            Logger.error('[Login Proof]: {}'.format(e))
        else:
            return response
