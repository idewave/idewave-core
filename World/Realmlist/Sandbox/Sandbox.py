from Realm.Realm import Realm
from Config.Run.config import Config
from Realm.Constants.RealmType import RealmType

# TODO: should be moved to db
realm = Realm(
    Config.Realm.Connection.WorldServer.realm_name,
    Config.Realm.Connection.WorldServer.host,
    Config.Realm.Connection.WorldServer.port,
    RealmType.NORMAL.value
)
