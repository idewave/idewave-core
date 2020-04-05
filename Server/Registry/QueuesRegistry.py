from Utils.Debug import Logger


class QueuesRegistry:

    def __getattr__(self, item):
        Logger.warning('[QueuesRegistry]: Trying to get unresolved attr {}'.format(item))
        pass
