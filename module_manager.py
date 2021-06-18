from patching.patch_manager import PatchManager
from utils.log_manager import LoggerManager
from settings.settings_manager import SettingsManager
from conf.config import ConfigManager
from request.request_manager import RequestManager
from request.api import APIManager
from request.auth_manager import AuthenticationManager
from gui.gui_manager import GUIManager
from heartbeat.heartbeatdata import HeartBeatManager
from scheduler.repeating_timer import RepeatingTimer
from utils.my_logger import logger


@logger
class BoxUpdateModule:
    def __init__(self):
        self.init_config()
        self.logger.info('BoxHelper Update Module is initializing...')
        self.init_managers()


    def init_config(self):
        self.settings_manager = SettingsManager()
        try:
            self.config_manager = ConfigManager()
        except KeyError:
            raise
        
    def init_managers(self):
        """
        initializing managers that handle API comm, authentication token, and abstracted HTTP requests
        """
        
        self.api_manager = APIManager()
        self.auth_manager = AuthenticationManager()
        self.request_manager = RequestManager()
        self.patch_manager = PatchManager()
        
        self.heartbeat_manager = HeartBeatManager() 
        # self.repeating_timer = RepeatingTimer(30.0, self.heartbeat_manager.send_heartbeat)

        

    # def do_stuff(self):
    #     self.logger.debug("Acquired token: %s", self.auth_manager.get_token())
    #     self.request_manager.get_version_check()
    
    def start_gui(self):
        self.info('Starting GUI...')
        self.gui_manager = GUIManager(
            getUserToken=self.auth_manager.acquire_new_token,
            getVersionCheck=self.patch_manager.check_update)


if __name__ == '__main__':
    LoggerManager()
    module_manager = BoxUpdateModule()
    module_manager.start_gui()