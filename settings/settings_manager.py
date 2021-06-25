import configparser, os, logging
from conf.reg import reg_get_QTHZ_path
from misc.enumerators import FilePath, SettingsCategories, SettingsItems
from settings.consts import DEFAULT_FILE_TEMPLATE
from misc.decorators import singleton

@singleton
class SettingsManager():
    def __init__(self):
        self.logger = logging.getLogger("box_helper_common_logger")
        self.logger.info("Starting the settings manager...")
        self.__settings_path = "./settings/settings.ini"
        self.read_settings(self.__settings_path)
        self.read_QTHZ_inst_path()
        self.logger.info("Settings finished loading...")

    def get_paths(self):
        return {
            FilePath.CONFIG: self.qthz_inst_path+self.__config[SettingsCategories.PATHS.value][SettingsItems.CONFIG.value],
            FilePath.FS: self.__config[SettingsCategories.PATHS.value][SettingsItems.FS.value],
            FilePath.JAVA: self.__config[SettingsCategories.PATHS.value][SettingsItems.JAVA.value],
            FilePath.JAR: self.__config[SettingsCategories.PATHS.value][SettingsItems.JAR.value]
        }

    def get_heartbeat_timer(self):
        return self.__config[SettingsCategories.TIMER.value][SettingsItems.HB.value]

    def get_versioncheck_timer(self):
        return self.__config[SettingsCategories.TIMER.value][SettingsItems.VC.value] 

    def get_env(self):
        return self.__config[SettingsCategories.GENERAL.value][SettingsItems.ENV.value]

    def get_logging_level(self):
        return self.__config[SettingsCategories.GENERAL.value][SettingsItems.LOGGING.value]

    def get_QTHZ_inst_path(self):
        return self.qthz_inst_path

    def get_sqlite_db_path(self):
        return self.qthz_inst_path+self.__config[SettingsCategories.PATHS.value]['data']

    def get_backup_dir_path(self):
        return self.qthz_inst_path+self.__config[SettingsCategories.PATHS.value]['backup']

    def get_patch_dir_path(self):
        return self.qthz_inst_path+self.__config[SettingsCategories.PATHS.value][SettingsItems.PATCH.value]

    def get_patch_meta_path(self):
        return self.get_patch_dir_path()+self.__config[SettingsCategories.PATHS.value][SettingsItems.PATCHMETA.value]

    def read_QTHZ_inst_path(self):
        self.qthz_inst_path = reg_get_QTHZ_path()

    def read_settings(self, path):
        self.verify_config_file_existence(path)
        self.__config = self.read_ini_into_config(path)

    def verify_config_file_existence(self, path):
        if not os.path.isfile(path):
            self.logger.warning(f"Settings file at {path} doesn't exist, creating default settings...")
            with open(path, "x") as settings_file:
                settings_file.write(DEFAULT_FILE_TEMPLATE)

    def read_ini_into_config(self, path):
        config = configparser.ConfigParser()
        config.read(path, encoding="UTF-8")
        return config
    
    def write_config_to_ini_file(self, config, filepath):
        with open(filepath, 'w') as configfile:
            config.write(configfile)
        self.logger.debug("保存配置完成")
    

        