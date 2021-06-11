import logging, configparser
from conf.consts import CONFIG, Envs
from base_manager import BaseManager

class ConfigManager(BaseManager):

    def __init__(self, path_manager, env):
        super().__init__(env)

        self.__host_address = CONFIG[env]['host_addr']
        self.__api_prefix = CONFIG[env]['api_prefix']

        self.config = self.read_ini_configs(path_manager.get_ini_path())
        self.__appkey = self.config['appkey']['key']
        self.__access_id = self.config['accessid']['id']
        self.__access_key_secret = self.config['accesssecret']['secret']
        self.logger.debug('Config Manager successfully initialized...')

    def get_host_address(self):
        return self.__host_address
    
    def get_api_prefix(self):
        return self.__api_prefix

    def get_keys(self):
        return {
            'appkey': self.__appkey, 
            'accessId': self.__access_id, 
            'accessKeySecret': self.__access_key_secret
        }

    def get_version_info(self):
        return {'versionNum': '1.2', 'versionCode':'v13111'}

    def read_ini_configs(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        return config
