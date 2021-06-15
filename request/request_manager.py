from misc.exceptions import HttpRequestError, ICBRequestError
import requests
from base_manager import BaseManager

class RequestManager(BaseManager):

    def __init__(self, config_manager, api_manager, auth_manager, env):
        super().__init__(env)
        self.config_manager = config_manager
        self.host_addr = config_manager.get_host_address()
        self.api_prefix = config_manager.get_api_prefix()
        self.api_manager = api_manager
        self.auth_manager = auth_manager

        self.logger.debug(f"{self.module_name} successfully initialized...")

    def get_version_check(self):
        auth = {
            # 'token': self.auth_manager.get_token(), 
            'appkey': self.config_manager.get_keys()['appkey']
        }
        version_info = self.config_manager.get_version_info()
        try:
            content = self.api_manager.get_version_check(auth, version_info['versionNum'])
        except HttpRequestError as err:
            self.logger.error("%s", err)
            return 
        except ICBRequestError as err:
            self.logger.error("%s", err)
            return 
        
        upgrade_mark = content['upgradeMark']
        upgrade_list = content['upgradeList']
        self.logger.debug("upgrade mark: %s, upgrade list: %s", upgrade_mark, upgrade_list)
        return content

