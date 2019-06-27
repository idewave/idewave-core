import time


class Timer(object):

    @staticmethod
    def get_ms_time():
        return int(time.time())
