import requests
from base_manager import BaseManager
from conf.reg import reg_get_QTHZ_path

class PathManager(BaseManager):

    def __init__(self, env):
        super().__init__(env)
        self.__ini_path = "\\conf\\configuration.ini"
        self.__fs_path = ""
        self.__jvm_path = ""
        self.__jar_path = ""
        self.get_QTHZ_inst_path()

    def get_ini_path(self):
        return self.qthz_inst_path+self.__ini_path

    def get_QTHZ_inst_path(self):
        self.qthz_inst_path = reg_get_QTHZ_path()