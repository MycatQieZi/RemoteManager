from misc.decorators import singleton
from request.auth_manager import AuthenticationManager
from request.api import APIManager
from conf.config import ConfigManager
from misc.exceptions import HttpRequestError, ICBRequestError
from utils.my_logger import logger
import requests

@singleton
@logger
class RequestManager():
    def __init__(self):
        self.config_manager = ConfigManager()
        self.host_addr = self.config_manager.get_host_address()
        self.api_prefix = self.config_manager.get_api_prefix()
        self.api_manager = APIManager()
        self.auth_manager = AuthenticationManager()

        self.logger.debug(f"{self.module_name} successfully initialized...")

    def get_version_check(self):
        auth = {
            # 'token': self.auth_manager.get_token(),
            'appkey': self.config_manager.get_keys()['appkey']
        }
        version_info = self.config_manager.get_version_info()
        try:
            content = self.api_manager.get_version_check(
                auth, version_info['versionNum'])
        except HttpRequestError as err:
            self.logger.error("%s", err)
            return
        except ICBRequestError as err:
            self.logger.error("%s", err)
            return

        upgrade_mark = content['upgradeMark']
        upgrade_list = content['upgradeList']
        self.logger.debug("upgrade mark: %s, upgrade list: %s", upgrade_mark,
                          upgrade_list)
        return content

    def post_heartbeat_info(self, heartbeat_info):
        auth = {
            'token': self.auth_manager.get_token(),
            'appkey': self.config_manager.get_keys()['appkey']
        }
        try:
            content = self.api_manager.post_heartbeat_info(
                auth, heartbeat_info)

        except HttpRequestError as err:
            self.logger.error("%s", err)
            return
        except ICBRequestError as err:
            self.logger.error("%s", err)
            return
        # TODO: handling stuffs
        return content
