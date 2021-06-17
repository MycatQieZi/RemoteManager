import logging, configparser
from misc.decorators import singleton
from settings.settings_manager import SettingsManager
from conf.consts import CONFIG
from misc.enumerators import Envs, FilePath
from utils.my_logger import logger

@singleton
@logger
class ConfigManager():

    def __init__(self):
        settings_manager = SettingsManager()
        self.__host_address = CONFIG[self.env]['host_addr']
        self.__api_prefix = CONFIG[self.env]['api_prefix']
        self.config = settings_manager.read_ini_into_config(settings_manager.get_paths()[FilePath.CONFIG])
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
