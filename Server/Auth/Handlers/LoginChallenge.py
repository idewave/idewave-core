from os import urandom
from struct import unpack, pack

from Server.Auth.Crypto.SRP import SRP
from Server.Auth.Constants.LoginResult import LoginResult
from World.WorldPacket.Constants.LoginOpCode import LoginOpCode
from Account.AccountManager import AccountManager

from Exceptions.Wrappers.ProcessException import ProcessException


class LoginChallenge(object):

    LOGIN_CHAL_PACKET_FORMAT = '<BBx3sBBBBH3sB3sx4sBHBBBBBB%ds'
    PACKET_SIZE_WITHOUT_ACC_NAME = 33

    def __init__(self, **kwargs):
        self.data = kwargs.pop('data')

        self.unk_code = 0
        self.size = 0
        self.game_name = None
        self.version_major = 0
        self.version_minor = 0
        self.version_patch = 0
        self.version_build = 0
        self.os = None
        self.platform = None
        self.locale = None
        self.timezone = 0
        self.ip_addr = (0, 0, 0, 0)
        self.account_name_size = 0
        self.account_name = None

        self.connection = kwargs.pop('connection')

    @ProcessException
    async def process(self):
        self._parse_data()

        with AccountManager() as account_mgr:
            account = account_mgr.get(name=self.account_name).account

            if account is None:
                raise Exception('Account \'{}\' is not found'.format(self.account_name))

            account.os = self.os
            account.ip = '.'.join([str(i) for i in self.ip_addr])
            account.platform = self.platform
            account.timezone = self.timezone
            account.locale = self.locale

            account_mgr.update()

            self.connection.account = account

            return self._get_response()

    @ProcessException
    def _parse_data(self):
        def _decode_cstring(cstring, encoding='ascii'):
            if type(cstring) is bytes:
                return cstring.decode(encoding).strip('\x00')[::-1]
            else:
                return cstring

        packet_part_with_acc = (len(self.data) - LoginChallenge.PACKET_SIZE_WITHOUT_ACC_NAME)
        parsed_data = unpack(LoginChallenge.LOGIN_CHAL_PACKET_FORMAT % packet_part_with_acc, self.data)

        self.unk_code = parsed_data[0]
        self.size = parsed_data[1]
        self.game_name = _decode_cstring(parsed_data[2])
        self.version_major = parsed_data[4]
        self.version_minor = parsed_data[5]
        self.version_patch = parsed_data[6]
        self.version_build = parsed_data[7]
        self.platform = _decode_cstring(parsed_data[8])
        self.os = _decode_cstring(parsed_data[10])
        self.locale = _decode_cstring(parsed_data[11])
        self.timezone = parsed_data[12]
        self.ip_addr = parsed_data[15:19]
        self.account_name_size, account_name = parsed_data[19:]
        self.account_name = account_name.decode('ascii')

    @ProcessException
    def _get_response(self):
        self.connection.srp.generate_server_ephemeral(self.connection.account.verifier)

        generator = int.to_bytes(SRP.GENERATOR, 1, 'little')
        modulus = int.to_bytes(SRP.MODULUS, 32, 'little')
        server_eph = int.to_bytes(self.connection.srp.serv_ephemeral, 32, 'little')

        response = pack(
            '<2B32sB1sB32s32s16sB',
            0,
            LoginResult.SUCCESS.value,
            server_eph,
            len(generator),
            generator,
            len(modulus),
            modulus,
            self.connection.account.salt,
            urandom(16),
            0  # ?
        )

        return LoginOpCode.LOGIN_CHALL, [response]
