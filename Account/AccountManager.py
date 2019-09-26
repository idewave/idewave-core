from Account.model import Account
from Utils.Debug.Logger import Logger
from DB.Connection.LoginConnection import LoginConnection


class AccountManager(object):

    def __init__(self):
        self.account = None

    def create(self, **kwargs):
        name = kwargs.pop('name', '')
        password = kwargs.pop('password', '')

        self.account = Account(name=name, password=password)
        self.session.add(self.account)
        self.session.commit()

        return self

    # any field of account table can be used for search
    def get(self, **kwargs):
        if kwargs:
            try:
                self.account = self.session.query(Account).filter_by(**kwargs).first()
            except Exception as e:
                Logger.error('[AccountManager]: Error has occurred, account will be None, error: {}'.format(e))

        return self

    def update(self):
        self.session.commit()
        # remove account from current session to stop tracking and allow player saving
        # we should do changes to current account before player enter the world
        self.session.expunge(self.account)
        return self

    def delete(self, **kwargs):
        if kwargs:
            try:
                self.session.query(Account).filter_by(**kwargs).delete()
            except Exception as e:
                Logger.error('[AccountManager]: Error has occured on account delete, {}'.format(e))

        return self

    def delete_all(self):
        self.session.query(Account).delete()
        return self

    # enter/exit are safe, should be used instead of __del__
    def __enter__(self):
        connection = LoginConnection()
        self.session = connection.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
