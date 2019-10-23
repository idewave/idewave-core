class CharactersLimitError(Exception):

    def __init__(self):
        message = 'Max characters count equals to 10'
        super().__init__(message)