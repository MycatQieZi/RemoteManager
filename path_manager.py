import requests
from base_manager import BaseManager

class PathManager(BaseManager):

    def __init__(self, env):
        super().__init__(env)
        self.__ini_path = "C:\\Users\\sharefiles\\dockervolumes\\data\\key.ini"
        self.__fs_path = ""
        self.__jvm_path = ""
        self.__jar_path = ""

    def get_ini_path(self):
        return self.__ini_path