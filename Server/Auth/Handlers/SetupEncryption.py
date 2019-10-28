import asyncio

from io import BytesIO
from base64 import b64decode
from hashlib import sha1

from Account.AccountManager import AccountManager
from Server.Connection.Connection import Connection

from Server.Auth.Crypto.HeaderCrypt import HeaderCrypt

from Exceptions.Wrappers.ProcessException import ProcessException
from Utils.AccountNameParser import AccountNameParser


class SetupEncryption(object):

    __slots__ = ('data', 'connection', 'session_key')

    def __init__(self, **kwargs):
        self.data: bytes = kwargs.pop('data')
        self.connection: Connection = kwargs.pop('connection')
        self.session_key = None

    async def process(self) -> tuple:
        account_name, client_seed, client_hash = self._parse_data()
        while not self.session_key:
            self._set_session_key()

        server_hash = SetupEncryption._generate_server_hash(
            account_name,
            client_seed,
            self.connection.auth_seed,
            self.session_key
        )

        if server_hash == client_hash:
            self._setup_encryption(self.session_key)

        return None, None

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

    @ProcessException()
    def _set_session_key(self):
        key = '#{}-session-key'.format(self.connection.account.name)
        session_key = self.connection.session_keys[key]
        self.session_key = b64decode(session_key)

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
