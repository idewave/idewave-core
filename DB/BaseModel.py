import traceback
import base64

from sqlalchemy.ext.declarative import AbstractConcreteBase, as_declarative, declared_attr
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, VARBINARY, FLOAT, VARCHAR, TINYINT, MEDIUMINT, SMALLINT
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm.collections import InstrumentedList

from Utils.Debug.Logger import Logger


@as_declarative()
class BaseModel(AbstractConcreteBase):

    id = Column(INTEGER, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_identity': cls.__tablename__
        }

    @hybrid_method
    def to_json(self):
        exclude_keys = ['_sa_instance_state']
        result = {}
        try:
            for key in self.__dict__:
                if key not in exclude_keys:
                    if isinstance(self.__dict__[key], InstrumentedList):
                        result[key] = [obj.to_json() for obj in self.__dict__[key]]
                    elif isinstance(self.__dict__[key], BaseModel):
                        result[key] = self.__dict__[key].to_json()
                    elif isinstance(self.__dict__[key], (bytes, bytearray)):
                        pass
                    else:
                        result[key] = self.__dict__[key]
        except AttributeError as e:
            Logger.error('[Player]: {}'.format(e))
            raise e
        except Exception as e:
            traceback.print_exc()
        else:
            return result

    @staticmethod
    def column(**kwargs):
        _type = kwargs.pop('type', None)

        if _type is None:
            raise Exception('[DB/BaseModel]: type should be set')

        # https://stackoverflow.com/a/1814594
        length = kwargs.pop('length', 128)

        col = {
            'string': VARCHAR(length=length),
            'integer': INTEGER,
            'float': FLOAT,
            'varbinary': VARBINARY(length=length),
            'tinyint': TINYINT,
            'mediumint': MEDIUMINT,
            'smallint': SMALLINT,
        }[_type]

        foreign_key = kwargs.pop('foreign_key', None)

        if foreign_key:
            foreign_key = ForeignKey(foreign_key, onupdate='CASCADE', ondelete='CASCADE')
            return Column(col, foreign_key, **kwargs)

        return Column(col, **kwargs)
