from abc import *
class Account(metaclass=ABCMeta):
    def __init__(self, id, password, browser):
        self.id = id
        self.password = password
        self.browser = browser