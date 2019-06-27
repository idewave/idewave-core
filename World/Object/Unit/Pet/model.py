from World.Object.Unit.model import Unit
from World.Object.Constants.HighGuid import HighGuid


class Pet(Unit):

    def __init__(self):
        super().__init__()
        self.high_guid = HighGuid.HIGHGUID_PET.value
