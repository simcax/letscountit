'''Base class for letscountit'''

class basecounting:

    __version = "0.0.1"

    def __init__(self) -> None:
        pass

    def version(self):
        return self.__version

class counterthing:

    def __init__(self,uuid) -> None:
        self.uuid = uuid
        self.count = 0

    def up(self):
        self.count += 1

    
