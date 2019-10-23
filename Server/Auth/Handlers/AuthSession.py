from io import BytesIO
from struct import pack
from base64 import b64decode
from hashlib import sha1

from Account.AccountManager import AccountManager
from Server.Connection.Connection import Connection
from World.WorldPacket.Constants.WorldOpCode import WorldOpCode
from Server.Auth.Constants.ResponseCodes import ResponseCodes
from Server.Auth.Crypto.HeaderCrypt import HeaderCrypt

from Exceptions.Wrappers.ProcessException import ProcessException
from Utils.AccountNameParser import AccountNameParser


class AuthSession(object):

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data')
        self.connection: Connection = kwargs.pop('connection')

    async def process(self):
        account_name, client_seed, client_hash = self._parse_data()
        session_key = self._get_session_key()
        server_hash = AuthSession._generate_server_hash(
            account_name,
            client_seed,
            self.connection.auth_seed,
            session_key
        )

        if server_hash == client_hash:
            response = AuthSession._get_response()
            self._setup_encryption(session_key)

            return WorldOpCode.SMSG_AUTH_RESPONSE, [response]

        return None, None

    @staticmethod
    def _get_response():
        response = pack(
            '<BIBIB',
            ResponseCodes.AUTH_OK.value,
            0x00,                           # BillingTimeRemaining
            0x00,                           # BillingPlanFlags
            0x00,                           # BillingTimeRested
            0x01                            # Expansion, 0 - normal, 1 - TBC, must be set manually for each account
        )

        return response

    def _parse_data(self):
        tmp_buf = BytesIO(self.data)
        # client build
        tmp_buf.read(2)
        # remove next 6 unknown null-bytes (\x00)
        tmp_buf.read(6)
        account_name = AccountNameParser.parse(tmp_buf)

        with AccountManager() as account_mgr:
            self.connection.account = account_mgr.get(name=account_name).account

        client_seed = tmp_buf.read(4)
        client_hash = tmp_buf.read(20)

        return account_name, client_seed, client_hash

    @ProcessException
    def _get_session_key(self):
        key = '#{}-session-key'.format(self.connection.account.name)
        session_key = self.connection.session_keys[key]
        return b64decode(session_key)

    def _setup_encryption(self, session_key: bytes):
        self.connection.header_crypt = HeaderCrypt(session_key)

    @staticmethod
    def _generate_server_hash(account_name, client_seed, auth_seed, session_key):
        to_hash = (
            account_name.encode('ascii') +
            bytes(4) +
            client_seed +
            auth_seed +
            session_key
        )

        server_hash = sha1(to_hash).digest()
        return server_hash
