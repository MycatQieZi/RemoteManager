from threading import Lock
from misc.decorators import singleton
from utils.my_logger import logger

@singleton
@logger
class LockManager:
    def __init__(self):
        self.heartbeat_lock = Lock()
        self.version_check_lock = Lock()
        self.get_token_lock = Lock()
        self.install_update_lock = Lock()
