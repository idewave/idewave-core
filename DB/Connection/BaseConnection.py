from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class BaseConnection(object):

    def __init__(self, user=None, password=None, host=None, db_name=None):
        if not user or not password or not host or not db_name:
            raise Exception('[BaseConnection]: not enough params')

        engine = create_engine(
            'mysql://{user}:{password}@{host}/{db_name}'.format(
                user=user,
                password=password,
                host=host,
                db_name=db_name
            )
        )

        self.engine = engine

        session_factory = sessionmaker(expire_on_commit=False, bind=self.engine)
        Session = scoped_session(session_factory)

        self.session = Session()
