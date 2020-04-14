from Typings.Metaclasses.RegistryMetaclass import RegistryMetaclass


# Since classes are instances of type, we can create parent metaclass with a __setattr__ method
# https://stackoverflow.com/questions/39708662/how-does-setattr-work-with-class-attributes
class AbstractRegistry(metaclass=RegistryMetaclass):
    pass
