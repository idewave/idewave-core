from sqlalchemy import create_engine
from Config.Run.config import Config


def drop_db():
    engine = create_engine(
        'mysql://{user}:{password}@{host}'.format(
            user=Config.Database.Connection.username,
            password=Config.Database.Connection.password,
            host=Config.Database.Connection.host
        )
    )

    engine.execute('DROP DATABASE IF EXISTS {db_name}'.format(db_name=Config.Database.DBNames.realm_db))
    engine.execute('DROP DATABASE IF EXISTS {db_name}'.format(db_name=Config.Database.DBNames.world_db))
    engine.execute('DROP DATABASE IF EXISTS {db_name}'.format(db_name=Config.Database.DBNames.login_db))
