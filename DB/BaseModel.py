import re
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.declarative.api import DeclarativeMeta

from Typings.Abstract.AbstractObservable import AbstractObservable


pattern = re.compile(r'(?<!^)(?=[A-Z])')


# https://stackoverflow.com/questions/28799089/python-abc-multiple-inheritance
# https://stackoverflow.com/a/100146/5397119 (about type)
class BaseModelMetaclass(DeclarativeMeta, type(AbstractObservable)):
    pass


class BaseModel(declarative_base(), AbstractObservable, metaclass=BaseModelMetaclass):

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


class LoginModel(BaseModel):

    __abstract__ = True

    @declared_attr
    def __table_args__(self):
        return {
            'schema': self.from_config("database:names:login_db")
        }


class WorldModel(BaseModel):

    __abstract__ = True

    @declared_attr
    def __table_args__(self):
        return {
            'schema': self.from_config("database:names:world_db")
        }


class RealmModel(BaseModel):

    __abstract__ = True

    @declared_attr
    def __table_args__(self):
        return {
            'schema': self.from_config("database:names:realm_db")
        }
