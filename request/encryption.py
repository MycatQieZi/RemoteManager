from base_manager import BaseManager


class EncryptionManager(BaseManager):
    def __init__(self, env):
        super().__init__(env)

    def encrypt(self, string_raw):
        return string_raw

    def decrypt(self, string_raw):
        return string_raw
