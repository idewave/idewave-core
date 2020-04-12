import re
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from Typings.Abstract.AbstractObservable import AbstractObservable


pattern = re.compile(r'(?<!^)(?=[A-Z])')


class Base(declarative_base(), AbstractObservable):

    __abstract__ = True

    @declared_attr
    def __tablename__(self):
        """
        Translates CamelCase table name into snake_case in lower case and adds 's' at the end for plural.
        For some cases (to comply with literacy) we need manually set __tablename__ attribute.

        For example, UnitTemplate -> unit_templates
        """
        return f'{pattern.sub("_", self.__name__).lower()}s'

    @declared_attr
    def __mapper_args__(self):
        return {
            'polymorphic_identity': self.__tablename__
        }


class LoginModel(Base):

    __abstract__ = True

    @declared_attr
    def __table_args__(self):
        return {
            'schema': self.from_config("database:names:login_db")
        }


class WorldModel(Base):

    __abstract__ = True

    @declared_attr
    def __table_args__(self):
        return {
            'schema': self.from_config("database:names:world_db")
        }


class RealmModel(Base):

    __abstract__ = True

    @declared_attr
    def __table_args__(self):
        return {
            'schema': self.from_config("database:names:realm_db")
        }
