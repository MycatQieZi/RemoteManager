import sys, logging

from conf.config import ConfigManager
from request.request_manager import RequestManager
from request.api import APIManager
from request.auth_manager import AuthenticationManager
from path_manager import PathManager
from base_manager import BaseManager
from gui.gui_manager import GUIManager
from heartbeat.heartbeatdata import HeartBeatManager
from scheduler.repeating_timer import RepeatingTimer
from conf.consts import Envs


class BoxUpdateModule(BaseManager):
    def __init__(self, env):
        super().__init__(env=env)
        self.init_config()
        self.logger.info('BoxHelper Update Module is initializing...')
        self.init_managers()


    def init_config(self):
        self.path_manager = PathManager(self.env)
        try:
            self.config_manager = ConfigManager(self.path_manager, self.env)
        except KeyError:
            raise
        
    def init_managers(self):
        """
        initializing managers that handle API comm, authentication token, and abstracted HTTP requests
        """
        
        self.api_manager = APIManager(self.config_manager, self.env)
        self.auth_manager = AuthenticationManager(self.api_manager, self.config_manager, self.env)
        self.request_manager = RequestManager(
            self.config_manager, self.api_manager, self.auth_manager, self.env)
        
        self.heartbeat_manager = HeartBeatManager(self.config_manager, self.request_manager, self.env) 
        self.repeating_timer = RepeatingTimer(30.0, self.heartbeat_manager.send_heartbeat())

        

    # def do_stuff(self):
    #     self.logger.debug("Acquired token: %s", self.auth_manager.get_token())
    #     self.request_manager.get_version_check()
    
    def start_gui(self):
        self.logger.info('BoxHelper Update Module is starting...')
        self.gui_manager = GUIManager(
            self.env,
            getUserToken=self.auth_manager.acquire_new_token,
            getVersionCheck=self.request_manager.get_version_check)


if __name__ == '__main__':
    module_manager = BoxUpdateModule(Envs.DEV)
    module_manager.start_gui()