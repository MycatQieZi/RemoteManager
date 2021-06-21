from misc.decorators import singleton
from utils.my_logger import logger
import rsa


@singleton
@logger
class EncryptionManager():
    def __init__(self):
        self.local_pubkey_path = 'conf/RSA/local/pubkey.pem' #本地RSA加密的公钥文件地址
        self.local_prikey_path = 'conf/RSA/local/prikey.pem' #本地RSA加密的私钥文件地址
        self.remote_pubkey_path = 'conf/RSA/remote/pubkey.pem'  # 配置中心RSA加密的公钥文件地址
        self.remote_prikey_path = 'conf/RSA/remote/prikey.pem'  # 配置中心RSA加密的私钥文件地址（本地实际上没有）
        
    def create_keys(self):
        pubkey, prikey = rsa.newkeys(1024)
        pubkey = pubkey.save_pkcs1()
        with open(self.local_pubkey_path, 'wb') as f_pubkey:
            f_pubkey.write(pubkey)
        prikey = prikey.save_pkcs1()
        with open(self.local_prikey_path, 'wb') as f_prikey:
            f_prikey.write(prikey)
        return (pubkey, prikey)
    
    def load_public_keys(self, path):
        with open(path, 'rb') as f:
            pubkey = f.read()
            pubkey = rsa.PublicKey.load_pkcs1(pubkey)
        return pubkey
    
    def load_private_key(self, path):
        with open(path, 'rb') as f:
            prikey = f.read()
            prikey = rsa.PrivateKey.load_pkcs1(prikey)
        return prikey
        
    def encrypt(self, content):
        pubkey = self.load_public_keys(self.remote_pubkey_path)
        crypto = rsa.encrypt(content, pubkey)
        return crypto

    def decrypt(self, crypto):
        prikey = self.load_private_key(self.local_prikey_path)
        content = rsa.decrypt(crypto, prikey)
        decoded_content = content.decode("utf-8")
        return decoded_content