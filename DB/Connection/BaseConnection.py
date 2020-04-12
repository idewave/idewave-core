from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from Config.Mixins import ConfigurableMixin


class BaseConnection(ConfigurableMixin):

    def __init__(self, **kwargs):

        connection_string = BaseConnection.build_connection_string(kwargs.pop('db_name'))

        engine = create_engine(connection_string)
        self.engine = engine

        session_factory = sessionmaker(expire_on_commit=False, bind=self.engine)
        self.session = scoped_session(session_factory)()

    # TODO: add cache for this
    @staticmethod
    def build_connection_string(db_name: str):
        base_connection_string = '{dialect}{driver}://' \
                                 '{user}:{password}@{host}:{port}' \
                                 '/{db_name}?charset={charset}'

        supported_dialects = BaseConnection.from_config('database:validation:supported_dialects')

        dialect = BaseConnection.from_config('database:connection:dialect')
        if dialect not in supported_dialects:
            raise Exception(f'Dialect "{dialect}" is not supported! Please check config.')

        if dialect == 'sqlite':
            in_memory = BaseConnection.from_config('database:connection:in_memory')
            if in_memory:
                return f'{dialect}://'

            absolute_path_to_db = BaseConnection\
                .from_config('database:connection:absolute_path_to_db')

            if not absolute_path_to_db:
                raise Exception(
                    'For sqlite driver you should specify in_memory option '
                    'or absolute path to db. Please check config.'
                )

            return f'{dialect}://{absolute_path_to_db}'

        driver = BaseConnection.from_config('database:connection:driver')
        supported_drivers = BaseConnection.from_config('database:validation:supported_drivers')
        if driver not in supported_drivers:
            raise Exception(f'Driver "{driver}" is not supported! Please check config.')

        if driver:
            driver = f'+{driver}'

        user = BaseConnection.from_config('database:connection:username')
        password = BaseConnection.from_config('database:connection:password')
        host = BaseConnection.from_config('database:connection:host')
        port = BaseConnection.from_config('database:connection:port')
        charset = BaseConnection.from_config('database:connection:charset')

        return base_connection_string.format(
            dialect=dialect,
            driver=driver,
            user=user,
            password=password,
            host=host,
            port=port,
            db_name=db_name,
            charset=charset,
        )
