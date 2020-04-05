from abc import ABC

from DB.Connection.RealmConnection import RealmConnection


class AbstractRealmManager(ABC):

    # enter/exit are safe, should be used instead of __del__
    def __enter__(self):
        connection = RealmConnection()
        self.session = connection.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        # https://stackoverflow.com/a/58590249/5397119
        return False
