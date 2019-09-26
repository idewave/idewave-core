class TempRef(object):

    __slots__ = ('account', 'player')

    def __init__(self, **kwargs):
        self.account = kwargs.pop('account', None)
        self.player = kwargs.pop('player', None)
