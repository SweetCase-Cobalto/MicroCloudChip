from account import Account
from user_info_interface import UserInfoInterface

class AccountManager(UserInfoInterface):
    def __init__(self):
        self.account_list = {}

    def login(self, id, password):
        pass
    
    def logout(self, id):
        pass
    
    def load_user_list(self):
        pass
    
    def update_user_list(self):
        pass
    
    @classmethod
    def change_pswd(self, id, new_pswd):
        pass