import requests, json

from request.encryption import EncryptionManager
from conf.consts import CONFIG
from base_manager import BaseManager
from misc.exceptions import HttpRequestError, ICBRequestError


class APIManager(BaseManager):
    def __init__(self, config_manager, env):
        super().__init__(env)
        self.enc_manager = EncryptionManager(env)
        self.config_manager = config_manager
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
        headers = {'appkey':auth['appkey'], 'token':auth['token']}
        params = {'appkey':auth['appkey'], 'versionNum':version_num}
        url = self.__assemble_url("/version/check")
        self.logger.debug("GET version check: %s", url)
        data = self.__http_get(url, params, headers)
        if not data['code'] == 1:
            raise ICBRequestError(data['msg'])
        return data['content']        

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
