from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, Float, ForeignKey, String

from DB.BaseModel import RealmModel
from Account.model import Account
from World.Object.Unit.model import AbstractUnit, Unit
from World.Object.Unit.Player.Skill.model import SkillTemplate
from World.Object.Unit.Spell.model import SpellTemplate

from World.Object.Constants.TypeMask import TypeMask
from World.Object.Constants.ObjectType import ObjectType
from World.Object.Constants.HighGuid import HighGuid
# from World.Region.model import Region


class AbstractPlayer(AbstractUnit):

    __abstract__ = True

    name = Column(String(20), unique=True, nullable=False)
    rage = Column(Integer)
    max_rage = Column(Integer)
    focus = Column(Integer)
    max_focus = Column(Integer)
    energy = Column(Integer)
    max_energy = Column(Integer)
    happiness = Column(Integer)
    max_happiness = Column(Integer)
    strength = Column(Integer)
    agility = Column(Integer)
    stamina = Column(Integer)
    intellect = Column(Integer)
    spirit = Column(Integer)
    block = Column(Float)
    dodge = Column(Float)
    parry = Column(Float)
    crit = Column(Float)
    race = Column(Integer)
    char_class = Column(Integer)
    gender = Column(Integer)
    skin = Column(Integer)
    face = Column(Integer)
    hair_style = Column(Integer)
    hair_color = Column(Integer)
    facial_hair = Column(Integer)


class Player(AbstractPlayer):

    player_id = Column('id', Integer, primary_key=True)

    player_flags = Column(Integer)
    player_bytes = Column(Integer)
    xp = Column(Integer)
    next_level_xp = Column(Integer)
    money = Column(Integer)

    @declared_attr
    def account_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:login_db")}.{Account.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    @declared_attr
    def unit_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:realm_db")}.{Unit.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    # @declared_attr
    # def region_id(self):
    #     return Column(
    #         Integer,
    #         ForeignKey(
    #             f'{self.from_config("database:names:world_db")}.{Region.__tablename__}.id',
    #             onupdate='CASCADE',
    #             ondelete='CASCADE'
    #         ),
    #         nullable=True
    #     )

    equipment = relationship('Equipment', lazy='subquery')
    unit = relationship('Unit', lazy='subquery')
    skills = relationship('PlayerSkill', lazy='subquery')
    spells = relationship('PlayerSpell', lazy='subquery')
    account = relationship('Account', lazy='subquery')
    # region = relationship('Region', lazy='subquery')

    @hybrid_property
    def object_type(self):
        return ObjectType.PLAYER.value

    @hybrid_property
    def type_mask(self):
        return TypeMask.PLAYER.value

    @hybrid_property
    def high_guid(self):
        return HighGuid.HIGHGUID_PLAYER.value


class PlayerSkill(RealmModel):

    id = Column(Integer, primary_key=True)

    @declared_attr
    def skill_template_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:world_db")}.{SkillTemplate.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    @declared_attr
    def player_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:realm_db")}.{Player.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    skill_template = relationship('SkillTemplate', lazy='subquery')
    player = relationship('Player', lazy='subquery')


class PlayerSpell(RealmModel):

    id = Column(Integer, primary_key=True)

    @declared_attr
    def spell_template_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:world_db")}.{SpellTemplate.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    @declared_attr
    def player_id(self):
        return Column(
            Integer,
            ForeignKey(
                f'{self.from_config("database:names:realm_db")}.{Player.__tablename__}.id',
                onupdate='CASCADE',
                ondelete='CASCADE'
            )
        )

    spell_template = relationship('SpellTemplate', lazy='subquery')
    player = relationship('Player', lazy='subquery')
