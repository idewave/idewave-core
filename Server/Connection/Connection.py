from Server.Auth.Crypto.SRP import SRP


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
        self.account = kwargs.pop('account', None)
        self.player = kwargs.pop('player', None)
        self.reader = kwargs.pop('reader', None)
        self.writer = kwargs.pop('writer', None)
        self.peername = kwargs.pop('peername', None)
        self.header_crypt = kwargs.pop('header_crypt', None)

        self.srp = SRP()
        self.auth_seed = kwargs.pop('auth_seed', None)
        self.session_keys = kwargs.pop('session_keys', None)

    def remove_auth_data(self):
        del self.srp
        del self.auth_seed
        del self.session_keys
