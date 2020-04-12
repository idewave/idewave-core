from DB.Connection.BaseConnection import BaseConnection


class LoginConnection(BaseConnection):

    def __init__(self):
        super().__init__(db_name=LoginConnection.from_config('database:names:login_db'))
