import sys, logging

from conf.config import ConfigManager
from request.request_manager import RequestManager
from request.api import APIManager
from request.auth_manager import AuthenticationManager
from path_manager import PathManager 
from base_manager import BaseManager
from gui.gui_manager import GUIManager
from conf.consts import Envs

class BoxUpdateModule(BaseManager):
    def __init__(self, env):
        super().__init__(env=env)
        self.init_config(env)
        self.logger.info('BoxHelper Update Module is initializing...')
        self.init_managers(env)
        self.start()


    def init_config(self, env):
        self.path_manager = PathManager(env)
        try:
            self.config_manager = ConfigManager(self.path_manager, env)
        except KeyError:
            raise
        
    def init_managers(self, env):
        """
        initializing managers that handle API comm, authentication token, and abstracted HTTP requests
        """
        
        self.api_manager = APIManager(self.config_manager, env)
        self.auth_manager = AuthenticationManager(self.api_manager, self.config_manager, env)
        self.request_manager = RequestManager(
            self.config_manager, self.api_manager, self.auth_manager, env)
        self.gui_manager = GUIManager(
            env,
            getUserToken=self.auth_manager.acquire_new_token,
            getVersionCheck=self.request_manager.get_version_check)

    def do_stuff(self):
        self.logger.debug("Acquired token: %s", self.auth_manager.get_token())
        self.request_manager.get_version_check()
    
    def start(self):
        self.logger.info('BoxHelper Update Module is starting...')
        self.do_stuff()


if __name__ == '__main__':
    update_module = BoxUpdateModule(Envs.DEV)
    # update_module.start()