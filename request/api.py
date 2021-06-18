from misc.decorators import singleton
from conf.config import ConfigManager
from request.encryption import EncryptionManager
from misc.exceptions import HttpRequestError, ICBRequestError
from utils.my_logger import logger

import requests, json, shutil

@singleton
@logger
class APIManager():
    def __init__(self):
        self.enc_manager = EncryptionManager()
        config_manager = ConfigManager()
        self.host_addr = config_manager.get_host_address()
        self.api_prefix = config_manager.get_api_prefix()

    def get_user_token(self, acc_id, acc_secret):
        params = {"accesskeyId":acc_id, "accesskeySecret":acc_secret}
        url = self.__assemble_url("/getUserToken", "/gateway/token")
        self.logger.debug("GET user token: %s", url)
        data = self.__http_get(url, params)
        if not data['code'] == 1:
            raise ICBRequestError(data['msg'])
        content = data['content']
        return content['token'], content['expireTime']

    def get_version_check(self, auth, version_num):
        headers = auth
        params = {'appkey':auth['appkey'], 'versionNum':version_num}
        url = self.__assemble_url("/version/check")
        self.logger.debug("GET version check: %s", url)
        data = self.__http_get(url, params, headers)
        if not data['code'] == 1:
            raise ICBRequestError(data['msg'])
        return data['content']   

    def get_file_download(self, auth, version_code):
        headers = auth
        params = {'appkey':auth['appkey'], 'versionCode':version_code}
        url = self.__assemble_url("/version/file")
        self.logger.debug("GET version file: %s", url)
        try:
            fname = self.__download_file(url, params, headers)
        except:
            self.error("File download failed") 
        
        return fname 

    def post_heartbeat_info(self, auth, heartbeat_info):
        headers = auth
        url = self.__assemble_url("/heartbeat")
        # add some logging
        data = self.__http_post(url, heartbeat_info, headers)
        # TODO: response handling
        return data

    def __assemble_url(self, url, api_prefix="default"):
        return self.host_addr + (self.api_prefix if api_prefix=="default" else api_prefix) + url

    def __http_post(self, url, data, headers={}): # header is a dict
        headers["Content-type"] = "application/json;charset=UTF-8"
        r = requests.post(url, data=data, headers=headers)
        if not r.status_code == 200:
            raise HttpRequestError(r)
        raw = r.text
        decrypted = self.enc_manager.decrypt(raw)
        try:
            parsed_dict = json.loads(decrypted)
        except json.decoder.JSONDecodeError:
            raise
        else:
            return parsed_dict

    def __http_get(self, url, params, headers=""):
        r = requests.get(url, params=params, headers=headers)
        if not r.status_code == 200:
            raise HttpRequestError(r)
        raw = r.text
        decrypted = self.enc_manager.decrypt(raw)
        try:
            parsed_dict = json.loads(decrypted)
        except json.decoder.JSONDecodeError:
            raise
        else:
            return parsed_dict

    def __download_file(self, url, params, headers=''):
        local_filename = params['versionCode']+".zip"
        with requests.get(url, params=params, headers=headers, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return local_filename
