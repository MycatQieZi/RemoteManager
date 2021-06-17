from misc.decorators import singleton
from utils.my_logger import logger

@singleton
@logger
class EncryptionManager():
    def __init__(self):
        pass

    def encrypt(self, string_raw):
        return string_raw

    def decrypt(self, string_raw):
        return string_raw
