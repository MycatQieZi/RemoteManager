from utils.log_manager import LoggerManager

def make_logger_methods_self(fn):
    def magical_wrapper(self, *args, **kwargs):
        fn(*args, **kwargs)
    return magical_wrapper

def logger(cls):
    log_manager = LoggerManager()
    env = log_manager.get_env()
    logger = log_manager.logger
    setattr(cls, 'env', env)
    setattr(cls, 'logger', logger)
    setattr(cls, 'module_name', cls.__name__)
    setattr(cls, 'info', make_logger_methods_self(logger.info))
    setattr(cls, 'debug', make_logger_methods_self(logger.debug))
    setattr(cls, 'warn', make_logger_methods_self(logger.warning))
    setattr(cls, 'error', make_logger_methods_self(logger.error))
    setattr(cls, 'critical', make_logger_methods_self(logger.critical))
    return cls