from processcontroller.processstatus import ProcessManager
from patching.install_manager import InstallManager
from patching.patch_manager import PatchManager
from utils.log_manager import LoggerManager
from settings.settings_manager import SettingsManager
from conf.config import ConfigManager
from request.request_manager import RequestManager
from request.api import APIManager
from request.auth_manager import AuthenticationManager
from gui.gui_manager import GUIManager
from gui.winrt_toaster import toast_notification
from heartbeat.heartbeatdata import HeartBeatManager
from scheduler.repeating_timer import RepeatingTimer
from scheduler.lock_manager import LockManager
from utils.my_logger import logger
import threading, sys


@logger
class BoxRemoteManager:
    def __init__(self):
        self.init_config()
        self.logger.info('BoxHelper Update Module is initializing...')
        self.init_managers()
        self.timers = []
        self.init_timers()


    def init_config(self):
        self.lock_manager = LockManager()
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
        self.install_manager = InstallManager()
        self.heartbeat_manager = HeartBeatManager() 
        self.process_manager = ProcessManager()

    def init_timers(self):
        heartbeat_interval = float(self.settings_manager.get_heartbeat_timer())
        self.heartbeat_timer = RepeatingTimer(
            heartbeat_interval, 
            self.heartbeat_manager.send_heartbeat)
        self.logger.debug("已启动自动心跳发送, timer interval: %.1f secs", heartbeat_interval)
        self.timers.append(self.heartbeat_timer)

        version_check_interval = float(self.settings_manager.get_version_check_timer())
        self.version_check_timer = RepeatingTimer(
            version_check_interval, 
            self.patch_manager.check_update)
        self.logger.debug("已启动自动版本检查, timer interval: %.1f secs", version_check_interval)
        self.timers.append(self.version_check_timer)
        
        self.heartbeat_timer.start()
        self.version_check_timer.start()
        
    def exit_gracefully(self, fn_child_exit):
        for timer in self.timers:
            timer.cancel()
        self.logger.debug("准备退出, 回收所有计时器...")
        fn_child_exit()

    # def do_stuff(self):
    #     self.logger.debug("Acquired token: %s", self.auth_manager.get_token())
    #     self.request_manager.get_version_check()

    def start_gui(self):
        self.info('Starting GUI...')
        toast_notification("证通智能精灵", "启动成功", "智能精灵助手已经启动, 并且在系统托盘后台运行")
        self.gui_manager = GUIManager(
            getUserToken=self.auth_manager.acquire_new_token,
            getVersionCheck=self.patch_manager.check_update,
            updateConfig=self.config_manager.load_config,
            sendHeartbeat=self.heartbeat_manager.send_heartbeat,
            clearCache=self.install_manager.clear_download_cache,
            installUpdate=self.install_manager.install_update,
            revertToLast=self.install_manager.revert_to_last,
            startQTHZ=self.process_manager.start_QTHZ,
            safeExit=self.exit_gracefully)
        
    def destroy(self):
        threads = threading.enumerate()
        for thread in threads:
            self.logger.debug("线程 %s 运行状态: %s", thread.name, thread.is_alive())
        toast_notification("证通智能精灵", "成功退出", "智能精灵助手已经停止")
        sys.exit(1)

def entrypoint():
    LoggerManager()
    module_manager = BoxRemoteManager()
    module_manager.start_gui()
    module_manager.destroy()
    

if __name__ == '__main__':
    entrypoint()