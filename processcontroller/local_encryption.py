from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from settings.settings_manager import SettingsManager
import os

# ---------------------生成密钥---------------------
# 需要，需要用这个进行解密
def generate_key(password, salt):
    return PBKDF2(password, salt, dkLen=32)

# ---------------------加密内容与处理---------------
# 这个应该需要，如果有配置需要更新，获取之后需要重新写入加密文件中去
def encrypt(text, key):
    pad = lambda s: s + b"\0" * (AES.block_size - len(s)%AES.block_size)
    text = pad(text)
    initialization = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CBC, initialization)
    return initialization + cipher.encrypt(text)
# ----------------------文件加密---------------------
# 需要
def file_encrypt(text, file_name, key):
    encrypted_text = encrypt(text, key)
    os.remove(file_name)
    with open(file_name, 'wb') as output_file:
        output_file.write(encrypted_text)
    
# -----------------------解密内容--------------------
# 需要，需要用这个来读取加密文件的内容并进行配置读取
def decrypt(encrypted_text, key):
    initialization = encrypted_text[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, initialization)
    plaintext = cipher.decrypt(encrypted_text[AES.block_size:])
    return plaintext.rstrip(b"\0")

# -------------------------文件内容解密------------------
# 需要
def file_decrypt(file_name, key):
    with open(file_name, 'rb') as input_file:
        encrypted_text = input_file.read()
    decrypted_text = decrypt(encrypted_text, key)
    #with open(file_name[:-4], 'wb') as output_file:
        #output_file.write(decrypted_text)
    #os.remove(file_name)
    return decrypted_text

# ----------------------------获取salt-----------
#需要，获取salt，进行密钥生成
def get_salt(file_name):
    with open(file_name, 'rb') as salt_file:
        salt = salt_file.read()
    return salt

        