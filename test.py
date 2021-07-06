from scheduler.repeating_timer import RepeatingTimer
#from module_manager import BoxUpdateModule
from utils.log_manager import LoggerManager
from heartbeat.heartbeatdata import HeartBeatManager
from request.encryption import EncryptionManager
from logsupload.logs_upload_module import LogsUploadManager

# def heartbeat_printer():
#     print("lol")
#
# LoggerManager()
# module_manager = BoxUpdateModule()
# heartbeat_manager = HeartBeatManager()
# repeating_timer = RepeatingTimer(3.0, heartbeat_printer)
# repeating_timer.start()
LoggerManager()
# encryptor = EncryptionManager()
# #encryptor.create_keys()
# a = encryptor.encrypt(b"hello")
# print(a)
# b = encryptor.decrypt(a)
# print(b)
logs_upload = LogsUploadManager()
logs_upload.send_logs(logs_upload.fs_log_path, logs_upload.fs_log_path_file)