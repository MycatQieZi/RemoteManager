from settings.settings_manager import SettingsManager
from misc.decorators import singleton
from conf.config import ConfigManager
from request.request_manager import RequestManager
from patching.patch_obj import PatchObject
from utils.my_logger import logger
from misc.enumerators import UpgradeMark, PatchCyclePhase
import os, jsonpickle, shutil

@singleton
@logger
class PatchManager:
    def __init__(self):
        self.state = PatchCyclePhase.READY
        jsonpickle.set_decoder_options('json', encoding='utf8')
        self.settings_manager = SettingsManager()
        self.request_manager = RequestManager()
        self.meta_file_path = self.settings_manager.get_patch_meta_path()

    def check_update(self):
        self.load_meta()
        if not self.state == PatchCyclePhase.READY:
            self.debug("Existing update sequence is in progress")
            return 0
        content = self.request_manager.get_version_check()
        return self.parse_version_info_response(content)

    def parse_version_info_response(self, content):
        try:
            upgrade_list = content['upgradeList']
        except:
            return 0

        self.patch_objs = map(PatchObject, upgrade_list)
        self.state = PatchCyclePhase.INCEPTION
        self.dump_meta()

        if(UpgradeMark(content['upgradeMark'])==UpgradeMark.MANDATORY):
            self.debug("Mandatory update")
            self.download()

    def download(self):
        self.state = PatchCyclePhase.DOWNLOAD
        self.debug("Mocking a download phase...")

    def check_exists(self, dir_or_file):
        return os.path.exists(dir_or_file)

    def dump_meta(self):
        meta_data = {
            'state': self.state,
            'list': self.patch_objs  
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
        with open(self.meta_file_path, 'r') as meta_file:
            json_str = meta_file.read()
        meta_data = jsonpickle.decode(json_str)
        self.state = meta_data['state']
        self.patch_objs = meta_data['list']
        self.debug('Loaded state from meta file')

    

    

    