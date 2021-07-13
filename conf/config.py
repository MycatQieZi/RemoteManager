import logging, configparser, traceback, copy

from PyQt5.QtCore import lowercasebase
from processcontroller.processstatus import FREESWITCH_PROCESS_NAME
from misc.decorators import singleton
from settings.settings_manager import SettingsManager
from conf.consts import CONFIG, REMOTE_CONF_MAPPING, XMLS, FS_CONF, FS_CONF_MAPPING
from misc.enumerators import Envs, FilePath
from utils.my_logger import logger
from lxml import etree

@singleton
@logger
class ConfigManager():

    def __init__(self):
        self.settings_manager = SettingsManager()
        # self.__host_address = CONFIG[self.env]['host_addr']
        self.__host_address = self.settings_manager.get_host_addr()
        self.__api_prefix = CONFIG[self.env]['api_prefix']
        self.tree_dict = {}
        self.fs_conf = copy.deepcopy(FS_CONF)
        self.paths = self.settings_manager.get_paths()
        # self.fs_conf_path = self.paths[FilePath.FS_CONF]
        self.load_config()
        self.logger.debug('Config Manager successfully initialized...')

    def load_config(self):
        try:
            self.config = self.settings_manager.read_ini_into_config(self.paths[FilePath.CONFIG])
            self.__version_num = self.config['QTHZ']['version']
            self.__version_code = self.config['QTHZ']['code']
            self.__appkey = self.config['appkey']['key']
            self.__access_id = self.config['accessid']['id']
            self.__access_key_secret = self.config['accesssecret']['secret']
        except Exception as e:
            self.logger.error(traceback.format_exc())
        else:
            self.logger.info("配置加载完成")

    def update_remote_config(self, arg_conf_map, version_num, version_code):
        self.logger.info("更新远程配置到本地")
        ini_file_path = self.paths[FilePath.CONFIG]
        config = self.settings_manager.read_ini_into_config(ini_file_path)
        config['QTHZ']['version'] = version_num
        config['QTHZ']['code'] = version_code
        for key, item in arg_conf_map.items():
            try:
                section, ini_key = REMOTE_CONF_MAPPING[key]
            except KeyError:
                self.logger.error("No mapping binded for key: %s", key)
                continue
            else:
                config[section][ini_key] = item
        self.settings_manager.write_config_to_ini_file(config, ini_file_path)
                    
    def get_host_address(self):
        return self.__host_address
    
    def get_callbox_addr(self):
        return self.get_config_item_by_mapping('callboxRealm')

    def get_api_prefix(self):
        return self.__api_prefix

    def get_keys(self):
        return {
            'appkey': self.__appkey, 
            'accessId': self.__access_id, 
            'accessKeySecret': self.__access_key_secret
        }

    def get_version_info(self):
        return {'versionNum': self.__version_num, 'versionCode': self.__version_code}

    def get_config_item_by_mapping(self, key):
        try:
            section, ini_key = REMOTE_CONF_MAPPING[key]
        except KeyError:
            self.logger.error("No mapping binded for key: %s", key)
            raise
        else:
            return self.config[section][ini_key]

# ---------------- FREESWITCH XML config update logic ------------------
    def save_fs_conf(self):
        self.logger.info("应用FreeSwitch配置")
        # get current fs config from xmls
        self.get_fs_config()
        # walk thru configuration.ini to get the new remote fs conf 
        fs_config_section = self.config['FreeSWITCH']
        for key in fs_config_section:
            gateway, param = FS_CONF_MAPPING[key.lower()]
            new_conf = fs_config_section[key]
            if(new_conf):
                self.fs_conf[gateway][param]['value'] = new_conf
        
        self.update_config(self.fs_conf)
        self.logger.debug("FS配置写入完成")

    def init_tree_dict_procedure(self):
        for filename in XMLS:
            try:
                self.logger.debug("读取FS配置: %s", self.paths[FilePath.FS_CONF] + filename)
                tree = etree.parse(self.paths[FilePath.FS_CONF] + filename)
            except OSError:
                raise
            else:
                self.tree_dict[tree.getroot()[0].get('name')] = tree

    def parse_fs_config(self):
        def operator_func(element, config_item): 
            config_item['value'] = element.get('value')
        
        self.trees_walker(self.tree_dict, operator_func, self.fs_conf)

    def get_new_fs_config(self):
        self.init_tree_dict_procedure()
        self.parse_fs_config()

    def get_fs_config(self):
        try:
            self.get_new_fs_config()      
        except OSError:
            self.logger.error("FS配置读取失败: %s", traceback.format_exc())
        else:
            self.logger.debug("最新FS配置: %s", self.fs_conf)
            return self.fs_conf

    def update_config(self, new_conf_obj):
        self.logger.debug("写入FS配置")
        def operator_func(element, config_item): 
            element.attrib['value'] = config_item['value']

        self.trees_walker(self.tree_dict,
            operator_func,
            new_conf_obj)

        for name, tree in self.tree_dict.items():
            try:
                tree.write(self.paths[FilePath.FS_CONF] + name + ".xml", pretty_print=True)
            except PermissionError:
                self.logger.error("FS配置写入失败, 配置文件没有写入权限")

    def trees_walker(self, trees, operator_func, fs_conf_obj):
        for tree_name, tree in trees.items():
            # sub_category = conf_obj[conf_type]
            gateway = tree.getroot()[0]
            for element in gateway:
                try:
                    config_item = fs_conf_obj[tree_name][element.get('name')]
                except:
                    continue
                else:
                    operator_func(element, config_item)
            