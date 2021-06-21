import os
import socket
from request.request_manager import RequestManager
from conf.config import ConfigManager
from utils.my_logger import logger

@logger
class LogsUploadManager():
    def __init__(self):
        self.config_manager = ConfigManager()
        self.request_manager = RequestManager()
        self.fs_log_path_file = r"C:\Program Files\FreeSWITCH\log\freeswitch.log"
        self.java_log_path_file = ""
        self.remote_manager_log_path_file = ""
        self.fs_log_path = "C:\\Program Files\\FreeSWITCH\\log\\"
        self.java_log_path = ""
        self.remote_manager_log_path = ""
        self.DEFAULT_FILE_SIZE = 1024 * 1024

    def check_logs_file_size(self, path):
        logs_file_size = os.path.getsize(path)
        if logs_file_size <= self.DEFAULT_FILE_SIZE:
            return [path]
        else:
            filename_list = self.file_cut_by_linecount(path, 8000)
            return filename_list
        
    def make_sub_file(self, lines, head, src_name, sub):
        [des_filename, ext_name] = os.path.splitext(src_name)
        filename = des_filename + '_' + str(sub) + ext_name
        f_out = open(filename, 'w')
        try:
            f_out.writelines([head])
            f_out.writelines(lines)
            return sub + 1, filename
        finally:
            f_out.close()
            
    def file_cut_by_linecount(self, filename, count):
        f_in = open(filename, 'r')
        try:
            head = f_in.readline()
            buf = []
            filename_list = []
            sub = 1
            for line in f_in:
                buf.append(line)
                if len(buf) == count:
                    sub, filename = self.make_sub_file(buf, head, filename, sub)
                    buf = []
                    filename_list.append(filename)
            if len(buf) != 0:
                _, filename = self.make_sub_file(buf, head, filename, sub)
                filename_list.append(filename)
            return filename_list
        finally:
            f_in.close()
            #return filename_list
            
    def send_logs(self, path, path_file):
        log_file_list = self.check_logs_file_size(path_file)
        for i in log_file_list:
            self.request_manager.post_logs_info(path, i)
        return None
        
    def delete_sended_logs(self):
        return None
    
        
        