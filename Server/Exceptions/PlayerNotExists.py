class PlayerNotExists(Exception):

    def __init__(self):
        message = 'It seems player was deleted'
        super().__init__(message)
