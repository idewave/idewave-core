from Realm.Realm import Realm
from Config.Run.config import Config
from Realm.CONSTANTS import RealmType

# TODO: should be moved to db
realm = Realm(
    Config.Realm.Connection.RealmServer.realm_name,
    Config.Realm.Connection.RealmServer.host,
    Config.Realm.Connection.RealmServer.port,
    RealmType.NORMAL.value
)
