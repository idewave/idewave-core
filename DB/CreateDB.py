from sqlalchemy import create_engine

from DB.Connection.LoginConnection import LoginConnection
from DB.Connection.WorldConnection import WorldConnection
from DB.Connection.RealmConnection import RealmConnection
from DB.BaseModel import BaseModel

from Config.Run.config import Config


def create_db():
    engine = create_engine(
        'mysql://{user}:{password}@{host}'.format(
            user=Config.Database.Connection.username,
            password=Config.Database.Connection.password,
            host=Config.Database.Connection.host
        )
    )

    engine.execute('CREATE DATABASE IF NOT EXISTS {db_name}'.format(db_name=Config.Database.DBNames.login_db))
    engine.execute('CREATE DATABASE IF NOT EXISTS {db_name}'.format(db_name=Config.Database.DBNames.world_db))
    engine.execute('CREATE DATABASE IF NOT EXISTS {db_name}'.format(db_name=Config.Database.DBNames.realm_db))


def create_tables():
    BaseModel.metadata.create_all(LoginConnection().engine)
    BaseModel.metadata.create_all(WorldConnection().engine)
    BaseModel.metadata.create_all(RealmConnection().engine)
