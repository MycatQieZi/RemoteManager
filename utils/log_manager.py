import logging, sys, logging.handlers
from conf.consts import CONFIG
from misc.enumerators import Envs
from misc.decorators import singleton
from settings.settings_manager import SettingsManager, SettingsCategories, SettingsItems

LEVELS = { # all native logging lib levels in ascending order, higher = severer
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
    'crit': logging.CRITICAL
}

FORMAT_PATTERN = '[box_daemon,,,] %(asctime)-15s.%(msecs)d [%(levelname)s] %(process)d '+\
    '--- [%(threadName)s] %(module)s [%(lineno)d] : %(message)s'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


@singleton
class LoggerManager():

    def __init__(self):
        self.logger = logging.getLogger("box_helper_common_logger")
        self.settings_manager = SettingsManager()
        self.get_env = self.settings_manager.get_env
        logging_level = self.settings_manager.get_logging_level().lower()
        self.log_expiration_days = int(self.settings_manager.get_log_expiration())
        
        
        self.init_logger(self.switch_logging_level(logging_level), self.ignore_file_output(self.get_env()))
        
        self.logger.debug("Logging manager successfully instantiated")

    # config logger properties to log for both file and console
    def init_logger(self, level=logging.INFO, to_file=True):
        self.logger.setLevel(level)

        formatter = logging.Formatter(FORMAT_PATTERN, TIME_FORMAT)
        
        if(to_file):
            fileHandler = logging.handlers.TimedRotatingFileHandler('logs/out.log', when='d', interval=1, backupCount=self.log_expiration_days, encoding='utf-8')
            fileHandler.setLevel(level)
            fileHandler.setFormatter(formatter)
            self.logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(formatter)
        self.logger.addHandler(consoleHandler)

    def switch_logging_level(self, logging_level):
        return LEVELS.get(logging_level, logging.INFO)

    def ignore_file_output(self, env):
        return env!=Envs.DEV.value and env!=Envs.LOCAL.value