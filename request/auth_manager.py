from misc.decorators import singleton
from conf.config import ConfigManager
from request.api import APIManager
from utils.my_logger import logger

@singleton
@logger
class AuthenticationManager:

    def __init__(self):
        # init managers
        self.api_manager = APIManager()
        self.config_manager = ConfigManager()

        # acquire token for the first time
        # self.acquire_new_token()

        self.debug(f"{self.module_name} successfully initialized...")


    def get_token(self):
        return self.__token
    
    def acquire_new_token(self):
        keys = self.config_manager.get_keys()
        self.__token, self.__expiration_timestamp = self.api_manager.get_user_token(
            keys['accessId'], keys['accessKeySecret'])

