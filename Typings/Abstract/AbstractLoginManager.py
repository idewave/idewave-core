from Typings.Abstract.AbstractBase import AbstractBase
from DB.Connection.LoginConnection import LoginConnection


class AbstractLoginManager(AbstractBase):

    # enter/exit are safe, should be used instead of __del__
    def __enter__(self):
        connection = LoginConnection()
        self.session = connection.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return False
