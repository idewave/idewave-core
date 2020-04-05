from asyncio import StreamReader, StreamWriter

from Server.Auth.Crypto.SRP import SRP
from Account.model import Account
from World.Object.Unit.Player.model import Player


class Connection(object):

    __slots__ = (
        'account',
        'player',
        'reader',
        'writer',
        'peername',
        'srp',
        'auth_seed',
        'session_keys',
        'header_crypt'
    )

    def __init__(self, **kwargs):
        self.account: Account = kwargs.pop('account', None)
        self.player: Player = kwargs.pop('player', None)
        self.reader: StreamReader = kwargs.pop('reader', None)
        self.writer: StreamWriter = kwargs.pop('writer', None)
        self.peername: str = kwargs.pop('peername', None)
        self.header_crypt = kwargs.pop('header_crypt', None)

        self.srp: SRP = SRP()
        self.auth_seed: bytes = kwargs.pop('auth_seed', None)
        self.session_keys = kwargs.pop('session_keys', None)

    def remove_auth_data(self):
        del self.srp
        del self.auth_seed
        del self.session_keys
