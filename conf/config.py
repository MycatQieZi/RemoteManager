import logging, configparser, traceback
from misc.decorators import singleton
from settings.settings_manager import SettingsManager
from conf.consts import CONFIG, REMOTE_CONF_MAPPING
from misc.enumerators import Envs, FilePath
from utils.my_logger import logger

@singleton
@logger
class ConfigManager():

    def __init__(self):
        self.settings_manager = SettingsManager()
        self.__host_address = CONFIG[self.env]['host_addr']
        self.__api_prefix = CONFIG[self.env]['api_prefix']
        self.load_config()
        self.logger.debug('Config Manager successfully initialized...')

    def load_config(self):
        try:
            self.config = self.settings_manager.read_ini_into_config(self.settings_manager.get_paths()[FilePath.CONFIG])
            self.__version_num = self.config['QTHZ']['version']
            self.__version_code = self.config['QTHZ']['code']
            self.__appkey = self.config['appkey']['key']
            self.__access_id = self.config['accessid']['id']
            self.__access_key_secret = self.config['accesssecret']['secret']
        except Exception as e:
            self.logger.error(traceback.format_exc())
        else:
            self.logger.info("配置加载完成")

    def update_remote_config(self, arg_conf_map, version_num, version_code):
        self.logger.info("更新远程配置到本地")
        ini_file_path = self.settings_manager.get_paths()[FilePath.CONFIG]
        config = self.settings_manager.read_ini_into_config(ini_file_path)
        config['QTHZ']['version'] = version_num
        config['QTHZ']['code'] = version_code
        for key, item in arg_conf_map.items():
            try:
                section, ini_key = REMOTE_CONF_MAPPING[key]
            except KeyError:
                continue
            else:
                config[section][ini_key] = item
        self.settings_manager.write_config_to_ini_file(config, ini_file_path)

    def get_host_address(self):
        return self.__host_address
    
    def get_callbox_addr(self):
        return self.config['FreeSWITCH']['callboxRealm']

    def get_api_prefix(self):
        return self.__api_prefix

    def get_keys(self):
        return {
            'appkey': self.__appkey, 
            'accessId': self.__access_id, 
            'accessKeySecret': self.__access_key_secret
        }

    def get_version_info(self):
        return {'versionNum': self.__version_num, 'versionCode': self.__version_code}
