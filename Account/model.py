from sqlalchemy import Column, Integer, String, Binary

from DB.BaseModel import LoginModel


class Account(LoginModel):

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    salt = Column(Binary)
    verifier = Column(String(100))
    ip = Column(String(32), nullable=True)
    timezone = Column(Integer, nullable=True)
    os = Column(String(32), nullable=True)
    platform = Column(String(32), nullable=True)
    locale = Column(String(4))
