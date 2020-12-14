from abc import *
class UserInfoInterface(metaclass=ABCMeta):
    @abstractmethod
    def change_pswd(self, id, new_pswd):
        pass