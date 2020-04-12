from sqlalchemy import create_engine

from DB.Connection.LoginConnection import LoginConnection
from DB.Connection.WorldConnection import WorldConnection
from DB.Connection.RealmConnection import RealmConnection
from DB.BaseModel import Base
from World.Object.StaticObject.model import StaticObject, StaticObjectTemplate


# TODO: refactor into class
def create_db():
    connection_string = Config.Database.Connection.sqlalchemy_connection_string

    engine = create_engine(
        connection_string.format(
            user=Config.Database.Connection.username,
            password=Config.Database.Connection.password,
            host=Config.Database.Connection.host,
            # the query below does not needs db_name
            db_name=''
        )
    )

    query = 'CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'

    engine.execute(query.format(db_name=Config.Database.DBNames.login_db))
    engine.execute(query.format(db_name=Config.Database.DBNames.world_db))
    engine.execute(query.format(db_name=Config.Database.DBNames.realm_db))


def create_tables():
    Base.metadata.create_all(LoginConnection().engine)
    Base.metadata.create_all(WorldConnection().engine)
    Base.metadata.create_all(RealmConnection().engine)
