'''Base class for letscountit'''


class Basecounting:

    __version = "0.0.1"

    def __init__(self) -> None:
        pass

    def version(self):
        return self.__version


class Counterthing:

    def __init__(self,uuid,startCount=0) -> None:
        self.uuid = uuid
        self.count = startCount

    def up(self,count=1):
        if isinstance(count,int):
            self.count += count
        else:
            raise ValueError("count needs to be an int")

    
