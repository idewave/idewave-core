from os import urandom

from Auth.Crypto.SRP import SRP
from DB.BaseModel import BaseModel

from Config.Run.config import Config


class Account(BaseModel):

    name        = BaseModel.column(type='string', length=20, nullable=False, unique=True)
    salt        = BaseModel.column(type='varbinary')
    verifier    = BaseModel.column(type='string', length=100)
    ip          = BaseModel.column(type='string', length=32)
    timezone    = BaseModel.column(type='integer')
    os          = BaseModel.column(type='string', length=32)
    platform    = BaseModel.column(type='string', length=32)
    locale      = BaseModel.column(type='string', length=4)

    __mapper_args__ = {
        'polymorphic_identity': 'account'
    }

    __table_args__ = {
        'schema': Config.Database.DBNames.login_db
    }

    def __init__(self, name, password=None, salt=None, verifier=None):
        if not name:
            raise Exception('Account name should be specified!')

        self.name = name.upper()
        # password does not saves to DB
        self.password = password.upper()
        self.salt = salt
        self.verifier = verifier
        self.ip_addr = None
        # offset in minutes from UTC time
        self.timezone = None
        # operation system
        self.os = None
        self.platform = None
        self.locale = None
        self.id = None

        if not password:
            if not salt or not verifier:
                raise Exception('Password does not exists! Password is necessary for SRP data generation')
        else:
            if not salt or not verifier:
                ' True when create account '
                self._generate_srp_data()

    def _generate_srp_data(self):
        self.salt = urandom(32)
        self.verifier = SRP.generate_verifier(
                self.name,
                self.password,
                self.salt)
