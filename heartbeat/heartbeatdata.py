from scheduler.lock_manager import LockManager
from request.request_manager import RequestManager
from yamlmanager import GetYamlStruct
from processcontroller.processstatus import ProcessManager
from processcontroller.systeminfo import getSystemInfo
from conf.config import ConfigManager
from utils.my_logger import logger
from misc.decorators import singleton, with_lock
import traceback

@singleton
@logger
class HeartBeatManager():
    def __init__(self):
        self.config_manager = ConfigManager()
        self.request_manager = RequestManager()
        self.lock_manager = LockManager()
        self.proc_manager = ProcessManager()
        self.config_manager.load_config()

    def fill_heartbeat_struct(self):
        CONFIG_PATH = 'model/data.yml'
        struct = GetYamlStruct(CONFIG_PATH)
        auto_info = self.config_manager.get_keys()
        app_key = auto_info['appkey']
        access_id = auto_info['accessId']
        access_secret = auto_info['accessKeySecret']

        process_status = ProcessManager()
        freeswitch_status = process_status.is_freeswitch_running()
        java_status = 1 if process_status.is_java_running() else 0
        reg_info = process_status.freeswitch_status()

        system_info = getSystemInfo()
        cpu_rate_info = system_info.cpu_rate()
        mem_rate_info = system_info.mem_rate()
        mac_name_ip_info = system_info.mac_name_ip()

        #TODO:get version info
        struct.content.update
        struct.content['version'] = self.config_manager.get_version_info()['versionNum']
        struct.content['host_ip'] = mac_name_ip_info['addr']
        struct.content['callbox_ip'] = self.config_manager.get_callbox_addr()
        struct.content['app_key'] = app_key
        struct.content['access_id'] = access_id
        struct.content['access_secret'] = access_secret
        struct.content['Freeswitch'] = freeswitch_status
        struct.content['Reg_callbox'] = reg_info['reg_callbox']
        struct.content['Reg_numconvert'] = reg_info['reg_numconvert']
        struct.content['Java'] = java_status
        struct.content['cpu'] = cpu_rate_info
        struct.content['mem'] = mem_rate_info
        struct.content['media_storage'] = '2G'
        return struct.content
    
    def send_heartbeat(self):
        @with_lock(self.lock_manager.heartbeat_lock, logger=self.logger)
        @with_lock(self.lock_manager.install_update_lock, blocking=True, logger=self.logger)
        def send():
            self.logger.debug("发送心跳")
            self.proc_manager.keep_fs_alive()
            self.proc_manager.keep_java_alive()
            hb_info = self.fill_heartbeat_struct()
            try:
                self.request_manager.post_heartbeat_info(hb_info)
            except Exception as e:
                self.error(traceback.format_exc())
        send()



