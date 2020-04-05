import re
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from Config.Run.config import Config


pattern = re.compile(r'(?<!^)(?=[A-Z])')


class Base(declarative_base()):

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """
        Translates CamelCase table name into snake_case in lower case and adds 's' at the end for plural.
        For some cases (to comply with literacy) we need manually set __tablename__ attribute
        """
        return f'{pattern.sub("_", cls.__name__).lower()}s'

    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_identity': cls.__tablename__
        }


class LoginModel(Base):

    __abstract__ = True

    @declared_attr
    def __table_args__(cls):
        return {
            'schema': Config.Database.DBNames.login_db
        }


class WorldModel(Base):

    __abstract__ = True

    @declared_attr
    def __table_args__(cls):
        return {
            'schema': Config.Database.DBNames.world_db
        }


class RealmModel(Base):

    __abstract__ = True

    @declared_attr
    def __table_args__(cls):
        return {
            'schema': Config.Database.DBNames.realm_db
        }
