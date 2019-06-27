class TempRef(object):

    ''' Uses as temporary storage for passing some data by-reference '''

    def __init__(self, **kwargs):
        self.account = kwargs.pop('account', None)
        self.player = kwargs.pop('player', None)
