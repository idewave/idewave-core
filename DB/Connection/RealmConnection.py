from DB.Connection.BaseConnection import BaseConnection


class RealmConnection(BaseConnection):

    def __init__(self):
        super().__init__(db_name=RealmConnection.from_config('database:names:realm_db'))
