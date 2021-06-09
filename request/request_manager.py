import requests
from base_manager import BaseManager

class RequestManager(BaseManager):

    def __init__(self, config_manager, api_manager, auth_manager, env):
        super().__init__(env)
        self.config_manager = config_manager
        self.host_addr = config_manager.get_host_address()
        self.api_prefix = config_manager.get_api_prefix()

        self.logger.debug(f"{self.module_name} successfully initialized...")
