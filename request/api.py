from settings.settings_manager import SettingsManager
from misc.decorators import singleton
from conf.config import ConfigManager
from request.encryption import EncryptionManager
from misc.exceptions import HttpRequestError, ICBRequestError, FileDownloadError
from utils.my_logger import logger

import requests, json, shutil, traceback

@singleton
@logger
class APIManager():
    def __init__(self):
        self.enc_manager = EncryptionManager()
        self.settings_manager = SettingsManager()
        self.config_manager = ConfigManager()
        self.host_addr = self.config_manager.get_host_address()
        self.api_prefix = self.config_manager.get_api_prefix()

    def get_user_token(self, acc_id, acc_secret):
        params = {"accesskeyId":acc_id, "accesskeySecret":acc_secret}
        url = self.__assemble_url("/getUserToken", "/gateway/token")
        self.logger.debug("GET user token: %s", url)
        data = self.__http_get(url, params)
        if not data['code'] == 1:
            raise ICBRequestError(data['msg'])
        content = data['content']
        return content['token'], content['expireTime']

    def get_version_check(self, version_num):
        headers = {
            # 'token': self.auth_manager.get_token(),
            'appkey': self.config_manager.get_keys()['appkey']
        }
        params = {'appkey':headers['appkey'], 'versionNum':version_num}
        url = self.__assemble_url("/version/check")
        self.logger.debug("GET version check: %s", url)
        data = self.__http_get(url, params, headers)
        if not data['code'] == 1:
            raise ICBRequestError(data['msg'])
        return data['content']   

    def get_file_download(self, version_code, local_filename, fn_set_progress):
        headers = {
            # 'token': self.auth_manager.get_token(),
            'appkey': self.config_manager.get_keys()['appkey']
        }
        params = {'appkey':headers['appkey'], 'versionCode':version_code}
        url = self.__assemble_url("/version/file")
        self.logger.debug("GET version file: %s", url)
        try:
            fname = self.__download_file(
                url, params, headers=headers, fn_set_progress=fn_set_progress, local_filename=local_filename)
        except Exception as e:
            self.error("File download failed...")
            raise FileDownloadError(traceback.print_exc()) 
        
        return fname 

    def post_heartbeat_info(self, heartbeat_info):
        headers = {
            # 'token': self.auth_manager.get_token(),
            'appkey': self.config_manager.get_keys()['appkey']
        }
        url = self.__assemble_url("/heartbeat")
        # add some logging
        data = self.__http_post(url, heartbeat_info, headers)
        # TODO: response handling
        return data
    
    def post_logs_info(self, auth, logs_info):
        headers = auth
        url = self.__assemble_url("/logsdata")
        # add some logging
        data = self.__upload_file(url, logs_info, headers)
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
    
    def __upload_file(self, url, data, headers={}): # header is a dict
        headers["Content-type"] = data.content_type
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
        # decrypted = self.enc_manager.decrypt(raw)
        decrypted = raw
        try:
            parsed_dict = json.loads(decrypted)
        except json.decoder.JSONDecodeError:
            raise
        else:
            return parsed_dict

    def __download_file(self, url, params, headers='', **kwargs):
        file_size_dl = 0
        chunk_sz = 8192
        with requests.get(url, params=params, headers=headers, stream=True) as r:
            file_size = int(r.headers["Content-Length"])
            with open(kwargs['local_filename'], 'wb') as f:
            #     shutil.copyfileobj(r.raw, f)
                for chunk in r.iter_content(chunk_size=chunk_sz):
                    # if self.shutdown_flag.is_set():
                    #     break
                    file_size_dl += len(chunk)
                    f.write(chunk)
                    progress = int(file_size_dl * 100. // file_size)
                    if progress % 10 == 0:
                        kwargs['fn_set_progress'](progress)
        return 1
