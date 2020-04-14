from Utils.Debug import Logger


class RestrictExtraFieldsMetaclass(type):

    ALLOWED_FIELDS = ()

    def __setattr__(self, key, value):
        if key not in self.ALLOWED_FIELDS:
            pass

    def __getattr__(self, item):
        Logger.warning(f'[{self.__class__.__name__}]: Trying to get unresolved attr {item}')
        pass


# Since classes are instances of type, we can create parent metaclass with a __setattr__ method
# https://stackoverflow.com/questions/39708662/how-does-setattr-work-with-class-attributes
class InitRegistry(metaclass=RestrictExtraFieldsMetaclass):

    ALLOWED_FIELDS = (
        'main_config',
        'login_server',
        'world_server',
        'world_observer',
        'identifier_region_map',
        'region_octree_map',
    )
