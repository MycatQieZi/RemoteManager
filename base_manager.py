import logging, sys
from conf.consts import CONFIG, Envs

class BaseManager():

    def __init__(self, env=Envs.DEV):
        self.module_name = self.__class__.__name__
        self.logger = logging.getLogger(self.module_name)
        try:
            conf_dict = CONFIG[env]
        except KeyError:
            self.logger.error("Cannot read config from keyword env: %s", env)
        
        self.init_logger(self.module_name, conf_dict['logging'])

    # config logger properties to log for both file and console
    def init_logger(self, module_name, level=logging.INFO):
        self.logger.setLevel(level)

        formatPattern = f'[{module_name}] %(asctime)-15s [%(levelname)s] %(threadName)s : %(message)s'
        formatter = logging.Formatter(formatPattern)
        
        fileHandler = logging.FileHandler('update_module.log')
        fileHandler.setLevel(level)
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(formatter)
        self.logger.addHandler(consoleHandler)	
