from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from Config.Run.config import Config


class BaseConnection(object):

    def __init__(self, user=None, password=None, host=None, db_name=None):
        if not all([user, password, host, db_name]):
            raise Exception('[BaseConnection]: not enough params')

        connection_string = Config.Database.Connection.sqlalchemy_connection_string

        engine = create_engine(
            connection_string.format(
                user=user,
                password=password,
                host=host,
                db_name=db_name
            )
        )

        self.engine = engine

        session_factory = sessionmaker(expire_on_commit=False, bind=self.engine)
        self.session = scoped_session(session_factory)()
