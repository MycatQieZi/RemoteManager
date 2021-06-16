from yamlmanager import GetYamlStruct
from processcontroller.processstatus import getProcessStatus
from processcontroller.systeminfo import getSystemInfo
from conf.config import ConfigManager
from conf.consts import Envs
from path_manager import PathManager


class HeartBeatManager(BaseManager):
    def __init__(self, config_manager, request_manager, env):
        super().__init__(env)
        self.config_manager = config_manager
        self.request_manager = request_manager

    def fill_heartbeat_struct(self):
        CONFIG_PATH = 'model/data.yml'
        struct = GetYamlStruct(CONFIG_PATH)
        auto_info = self.config_manager.get_keys()
        app_key = auto_info['appkey']
        access_id = auto_info['accessId']
        access_secret = auto_info['accessKeySecret']

        process_status = getProcessStatus()
        freeswitch_status = process_status.isFreeSwitchRunning()
        java_status = process_status.isJavaRunning()
        reg_info = process_status.freeswitchStatus()

        system_info = getSystemInfo()
        cpu_rate_info = system_info.cpu_rate()
        mem_rate_info = system_info.mem_rate()
        mac_name_ip_info = system_info.mac_name_ip()

        #TODO:get version info
        struct.content.update
        struct.content['BasicInfo']['version'] = '1.2.1'
        struct.content['BasicInfo']['host_ip'] = mac_name_ip_info['addr']
        struct.content['BasicInfo']['callbox_ip'] = '192.168.65.176'
        struct.content['BasicInfo']['app_key'] = app_key
        struct.content['BasicInfo']['access_id'] = access_id
        struct.content['BasicInfo']['access_secret'] = access_secret
        struct.content['ServiceStatus']['Freeswitch'] = freeswitch_status
        struct.content['ServiceStatus']['Reg_callbox'] = reg_info['reg_callbox']
        struct.content['ServiceStatus']['Reg_numconvert'] = reg_info['reg_numconvert']
        struct.content['ServiceStatus']['Java'] = java_status
        struct.content['SystemInfo']['cpu'] = cpu_rate_info
        struct.content['SystemInfo']['mem'] = mem_rate_info
        struct.content['SystemInfo']['media_storage'] = '2G'
        return struct.content
    
    def send_heartbeat(self):
        hb_info = self.fill_heartbeat_struct()
        self.request_manager.post_heartbeat_info(hb_info)


