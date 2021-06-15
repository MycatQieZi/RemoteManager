from conf.consts import CONFIG, Envs
from base_manager import BaseManager

class AuthenticationManager(BaseManager):

    def __init__(self, api_manager, config_manager, env):
        super().__init__(env)
        
        # init managers
        self.api_manager = api_manager
        self.config_manager = config_manager

        # acquire token for the first time
        # self.acquire_new_token()

        self.logger.debug(f"{self.module_name} successfully initialized...")


    def get_token(self):
        return self.__token
    
    def acquire_new_token(self):
        keys = self.config_manager.get_keys()
        self.__token, self.__expiration_timestamp = self.api_manager.get_user_token(
            keys['accessId'], keys['accessKeySecret'])

