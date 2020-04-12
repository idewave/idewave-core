from DB.Connection.BaseConnection import BaseConnection


class WorldConnection(BaseConnection):

    def __init__(self):
        super().__init__(db_name=WorldConnection.from_config('database:names:world_db'))
