
class _GrowiCreds():
    """
    Contains GROWI login credentials
    """
    def __init__(self, user="", pw=""):
        self.__user = user
        self.__pw = pw

    @property
    def user(self):
        return self.__user
    
    @user.setter
    def user(self, value):
        self.__user = value
    
    @property
    def password(self):
        return self.__pw

    @password.setter
    def password(self, value):
        self.__pw = value
    

