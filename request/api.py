from settings.settings_manager import SettingsManager
from misc.decorators import singleton
from conf.config import ConfigManager
from request.encryption import EncryptionManager
from misc.exceptions import HttpRequestError, ICBRequestError, FileDownloadError, NoFileError
from utils.my_logger import logger

import requests, json, shutil, traceback, datetime

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
            raise ICBRequestError(data)
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
            raise ICBRequestError(data)
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
            fname = self.__download_in_chunks(
                url, params, headers=headers, fn_set_progress=fn_set_progress, local_filename=local_filename)
        except NoFileError as nfe:
            raise nfe 
        
        except ICBRequestError as icbe:
            self.logger.error("下载失败! 原因: %s", icbe.message)
            raise FileDownloadError(icbe.message) 
        
        except Exception as e:
            self.error("File download failed...")
            raise FileDownloadError(traceback.print_exc()) 
        
        return fname  

    def post_heartbeat_info(self, heartbeat_info):
        headers = {
            # 'token': self.auth_manager.get_token(),
            'appkey': self.config_manager.get_keys()['appkey']
        }
        heartbeat_key_val_list = list(map(lambda tup: {'key': tup[0], 'value': tup[1]}, heartbeat_info.items()))
        print(heartbeat_key_val_list)
        data = {
            "appkey": self.config_manager.get_keys()['appkey'],
            "items": list(heartbeat_key_val_list),
            "time": int(datetime.datetime.now().timestamp() * 1000),
            "versionCode": self.config_manager.get_version_info()['versionCode']
        }
        self.logger.debug("心跳包请求体：%s", data)
        url = self.__assemble_url("/heartBeat")
        # add some logging
        result = self.__http_post(url, data, headers)
        if not result['code'] == 1:
            raise ICBRequestError(result['msg'])
        return result
    
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
        r = requests.post(url, json=data, headers=headers, timeout=3)
        if not r.status_code == 200:
            raise HttpRequestError(r, r.text)
        raw = r.text
        # decrypted = self.enc_manager.decrypt(raw)
        decrypted = raw
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
            raise HttpRequestError(r, r.text)
        raw = r.text
        decrypted = self.enc_manager.decrypt(raw)
        try:
            parsed_dict = json.loads(decrypted)
        except json.decoder.JSONDecodeError:
            raise
        else:
            return parsed_dict
    
    

    def __http_get(self, url, params, headers=""):
        r = requests.get(url, params=params, headers=headers, timeout=3)
        if not r.status_code == 200:
            raise HttpRequestError(r, r.text)
        raw = r.text
        # decrypted = self.enc_manager.decrypt(raw)
        decrypted = raw
        try:
            parsed_dict = json.loads(decrypted)
            if not parsed_dict['code'] == 1:
                raise ICBRequestError(parsed_dict['msg'])
            parsed_dict['content'] = json.loads(parsed_dict['content'])
        except json.decoder.JSONDecodeError:
            raise
        else:
            return parsed_dict

    def __download_in_chunks(self, url, params, headers='', **kwargs):
        currentIndex = 0
        totalIndex = 10
        with open(kwargs['local_filename'], 'wb') as f:
            pass
        while not currentIndex == totalIndex:
            params['fileIndex'] = currentIndex
            r = requests.get(url, params=params, headers=headers, timeout=3)
            if not r.status_code == 200:
                raise HttpRequestError(r, r.text)
            raw = r.text
            try:
                parsed_dict = json.loads(raw)
                if not parsed_dict['code'] == 1:
                    raise ICBRequestError(parsed_dict['msg'])
                content = parsed_dict['content']
                totalIndex = content['totalIndex']
            except json.decoder.JSONDecodeError:
                raise

            else:
                with open(kwargs['local_filename'], 'ab') as f:
                    f.write(b''.join([int_byte.to_bytes(1, 'big', signed=True) for int_byte in content['bytes']]))
                currentIndex += 1
                kwargs['fn_set_progress'](currentIndex, totalIndex)
        return 1

    # deprecated download as stream
    def __download_file_stream_in_chunks(self, url, params, headers='', **kwargs):
        file_size_dl = 0
        chunk_sz = 8192
        with requests.get(url, params=params, headers=headers, stream=True) as r:
            try:
                file_size = int(r.headers["Content-Length"])
            except:
                raise NoFileError
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
