from sqlalchemy.ext.declarative import AbstractConcreteBase, as_declarative, declared_attr
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, VARBINARY, FLOAT, VARCHAR, TINYINT, MEDIUMINT, SMALLINT


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
