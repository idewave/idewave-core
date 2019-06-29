from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from DB.BaseModel import BaseModel
from World.Object.Unit.model import Unit
from World.Object.Constants.TypeMask import TypeMask
from World.Object.Constants.ObjectType import ObjectType
from World.Object.Constants.HighGuid import HighGuid

from World.Object.Unit.Player.Inventory.Equipment.model import Equipment

from Config.Run.config import Config


class Player(Unit):

    id                      = Unit.column(type='integer',
                                          foreign_key=Config.Database.DBNames.realm_db + '.unit.id',
                                          primary_key=True)
    name                    = Unit.column(type='string', unique=True, nullable=False)
    player_flags            = Unit.column(type='integer')
    skin                    = Unit.column(type='integer')
    face                    = Unit.column(type='integer')
    hair_style              = Unit.column(type='integer')
    hair_color              = Unit.column(type='integer')
    facial_hair             = Unit.column(type='integer')
    xp                      = Unit.column(type='integer')
    next_level_xp           = Unit.column(type='integer')
    block                   = Unit.column(type='float')
    dodge                   = Unit.column(type='float')
    parry                   = Unit.column(type='float')
    crit                    = Unit.column(type='float')
    money                   = Unit.column(type='integer')
    player_bytes            = Unit.column(type='integer')

    account_id              = Unit.column(type='integer',
                                          foreign_key=Config.Database.DBNames.login_db + '.account.id')

    unit                    = relationship('Unit', lazy='subquery')
    equipment               = relationship('Equipment', lazy='subquery')
    account                 = relationship('Account', lazy='subquery')

    __table_args__ = {
        'schema': Config.Database.DBNames.realm_db
    }

    @hybrid_property
    def object_type(self):
        return ObjectType.PLAYER.value

    @hybrid_property
    def type_mask(self):
        return TypeMask.PLAYER.value

    @hybrid_property
    def high_guid(self):
        return HighGuid.HIGHGUID_PLAYER.value


class PlayerSkill(BaseModel):

    __tablename__ = 'player_skill'

    skill_template_id               = BaseModel.column(type='integer',
                                                       foreign_key=Config.Database.DBNames.world_db + '.skill_template.id')

    player_id                       = BaseModel.column(type='integer',
                                                       foreign_key=Config.Database.DBNames.realm_db + '.player.id')

    __table_args__ = {
        'schema': Config.Database.DBNames.realm_db
    }


class PlayerSpell(BaseModel):

    __tablename__ = 'player_spell'

    spell_template_id               = BaseModel.column(type='integer',
                                                       foreign_key=
                                                            Config.Database.DBNames.world_db + '.spell_template.id')

    player_id                       = BaseModel.column(type='integer',
                                                       foreign_key=Config.Database.DBNames.realm_db + '.player.id')

    __table_args__ = {
        'schema': Config.Database.DBNames.realm_db
    }
