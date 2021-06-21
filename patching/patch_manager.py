from settings.settings_manager import SettingsManager
from misc.decorators import singleton
from conf.config import ConfigManager
from request.request_manager import RequestManager
from patching.patch_obj import PatchObject
from utils.my_logger import logger
from misc.enumerators import PatchStatus, UpgradeMark, PatchCyclePhase
from misc.exceptions import FileDownloadError
from pathlib import Path
import os, jsonpickle, shutil, hashlib, traceback

@singleton
@logger
class PatchManager:
    def __init__(self):
        self.state = PatchCyclePhase.READY
        jsonpickle.set_decoder_options('json', encoding='utf8')
        self.settings_manager = SettingsManager()
        self.request_manager = RequestManager()
        self.meta_file_path = self.settings_manager.get_patch_meta_path()
        self.retry = 5
        self.progress = 0

    def check_update(self):
        self.load_meta()
        # if not self.state == PatchCyclePhase.READY:
        #     self.debug("Existing update sequence is in progress")
        #     return 0
        self.info("当前下载流程状态: %s", self.state.name)
        if self.state == PatchCyclePhase.READY:
            status = self.check_for_update_phase()
        elif self.state == PatchCyclePhase.INCEPTION:
            status = self.file_download_phase()
        
        if(status==0): # something went wrong
            self.retry_once()
            self.dump_meta()
            return 
        

    def check_for_update_phase(self):
        try:
            content = self.request_manager.get_version_check()
            self.logger.debug("查询版本回餐: %s",content)
            upgrade_list = content['upgradeList']
            self.upgrade_mark = content['upgradeMark']
        except Exception as err:
            self.logger.error("%s", traceback.format_exc())
            self.state = PatchCyclePhase.READY
            return 0

        self.patch_objs = list(map(PatchObject, upgrade_list))
        self.dump_meta()
        print(self.patch_objs)
          
        self.state = PatchCyclePhase.INCEPTION
        return self.file_download_phase()

    def file_download_phase(self):
        # self.logger.debug("content: %s", content)
        self.state = PatchCyclePhase.DOWNLOAD
        if(UpgradeMark(self.upgrade_mark)==UpgradeMark.MANDATORY):
            self.debug("Mandatory update")
            try:
                for index, patch_obj in enumerate(self.patch_objs):
                    self.download_one(self.patch_objs[index])
            except FileDownloadError as err:
                self.logger.error("下载失败! 原因: %s", err)
                self.state = PatchCyclePhase.INCEPTION
                return 0
            self.debug("Download finished.")
            self.state = PatchCyclePhase.PENDING
        return 1  

    def download_one(self, patch_obj):
        if(patch_obj.status==PatchStatus.DOWNLOADED):
            return
        patch_obj.status = PatchStatus.DOWNLOADING
        file_dir = f"{self.settings_manager.get_patch_dir_path()}\\{patch_obj.version_num}"
        file_name = f"\\{patch_obj.version_code}.zip"
        full_path = file_dir + file_name
        Path(file_dir).mkdir(parents=True, exist_ok=True)
        self.progress = 0
        self.request_manager.get_file_download(
            patch_obj.version_code, full_path, self.check_dl_progress)
        md5 = self.gen_md5(full_path)
        self.debug("远程文件MD5值: %s", patch_obj.file_MD5)
        self.debug("本地文件MD5值: %s", md5)
        if not md5==patch_obj.file_MD5:
            raise FileDownloadError(f"文件完整性校验失败: {patch_obj.version_num}/{patch_obj.version_code}")
        patch_obj.status = PatchStatus.DOWNLOADED

    def check_exists(self, dir_or_file):
        return os.path.exists(dir_or_file)

    def dump_meta(self):
        meta_data = {
            'state': self.state,
            'list': self.patch_objs,
            'retries': self.retry,
            'mark': self.upgrade_mark
        }
        data_json_str = jsonpickle.encode(meta_data)
        file_flag = 'w'
        if not os.path.isfile(self.meta_file_path):
            self.logger.debug('Creating new meta file')
            file_flag = 'x'
        with open(self.meta_file_path, file_flag) as meta_file:
            meta_file.write(data_json_str)
            self.debug('Update state is saved in meta file')

    def load_meta(self):
        try:
            with open(self.meta_file_path, 'r') as meta_file:
                json_str = meta_file.read()
        except FileNotFoundError:
            self.warn("Could not find download meta file, previous states might not be preserved")
            return 
        meta_data = jsonpickle.decode(json_str)
        self.state = meta_data['state']
        self.patch_objs = meta_data['list']
        self.retry = meta_data['retries']
        self.upgrade_mark = meta_data['mark']
        self.debug('Loaded state from meta file')

    def retry_once(self):
        self.retry -= 1
        if(self.retry < 0):
            self.state = PatchCyclePhase.READY
            self.retry = 5

    def check_dl_progress(self, progress):
        if not progress == self.progress:
            self.progress = progress
            self.info(f"Download progress: {self.progress}%")

    def gen_md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    

    