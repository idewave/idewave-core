class RegistryMetaclass(type):

    _initialized = False

    keys = ()

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if cls.keys:
            # initializing registry keys
            for key in cls.keys:
                setattr(cls, key, None)

            # not allow to add new keys
            cls._initialized = True
            # remove already redundant attr
            del cls.keys

    def __setattr__(self, key, value):
        # not allow to set key for classes without not empty keys attribute
        if hasattr(self, key) or (not self._initialized and self.keys):
            super().__setattr__(key, value)
        else:
            raise AttributeError(
                f'You can\'t set attribute that missed in {self.__class__.__name__}'
            )
