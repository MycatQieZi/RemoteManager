from misc.decorators import singleton
from request.auth_manager import AuthenticationManager
from request.api import APIManager
from conf.config import ConfigManager
from misc.exceptions import FileDownloadError, HttpRequestError, ICBRequestError
from utils.my_logger import logger
from requests_toolbelt import MultipartEncoder
import requests


@singleton
@logger
class RequestManager():
    def __init__(self):
        self.config_manager = ConfigManager()
        self.host_addr = self.config_manager.get_host_address()
        self.api_prefix = self.config_manager.get_api_prefix()
        self.api_manager = APIManager()

        self.logger.debug(f"{self.module_name} successfully initialized...")

    def get_version_check(self):
        version_info = self.config_manager.get_version_info()
        content = self.api_manager.get_version_check(version_info['versionNum'])

        upgrade_mark = content['upgradeMark']
        upgrade_list = content['upgradeList']
        self.logger.debug("upgrade mark: %s, upgrade list: %s", upgrade_mark,
                          upgrade_list)
        return content
    
    def get_file_download(self, version_code, local_filename, fn_set_progress):
        return self.api_manager.get_file_download(version_code, local_filename, fn_set_progress)

    def post_heartbeat_info(self, heartbeat_info):
        try:
            content = self.api_manager.post_heartbeat_info(heartbeat_info)

        except HttpRequestError as err:
            self.logger.error("%s", err)
            return
        except ICBRequestError as err:
            self.logger.error("%s", err)
            return
        # TODO: handling stuffs
        return content

    def post_logs_info(self, path, filename):
        auth = {
            'token': self.auth_manager.get_token(),
            'appkey': self.config_manager.get_keys()['appkey']
        }
        data = MultipartEncoder(
            fields={
                'propertyMessageXml': ('filename', open(path + filename, 'rb'),
                                       'text/xml')
            })
        try:
            content = self.api_manager.post_logs_info(auth, data)

        except HttpRequestError as err:
            self.logger.error("%s", err)
            return
        except ICBRequestError as err:
            self.logger.error("%s", err)
            return
        # TODO: handling stuffs
        return content
