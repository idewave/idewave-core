from DB.Connection.BaseConnection import BaseConnection

from Config.Run.config import Config


class RealmConnection(BaseConnection):

    def __init__(self):
        super().__init__(
            user=Config.Database.Connection.username,
            password=Config.Database.Connection.password,
            host=Config.Database.Connection.host,
            db_name=Config.Database.DBNames.realm_db
        )
