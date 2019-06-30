from sqlalchemy import create_engine

from Config.Run.config import Config


def drop_db():
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

    query = 'DROP DATABASE IF EXISTS {db_name}'

    engine.execute(query.format(db_name=Config.Database.DBNames.realm_db))
    engine.execute(query.format(db_name=Config.Database.DBNames.world_db))
    engine.execute(query.format(db_name=Config.Database.DBNames.login_db))
