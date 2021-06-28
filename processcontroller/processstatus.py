from misc.enumerators import FilePath
from settings.settings_manager import SettingsManager
from utils.my_logger import logger
from misc.decorators import singleton
import os
import subprocess
import traceback
import psutil

FREESWITCH_PROCESS_NAME = 'FreeSwitch'
JAVA_PROCESS_PORT = '18080'
ICB_BOX_JAVA__PROC_NAME = 'java'

@singleton
@logger
class ProcessManager:
    def __init__(self):
        start = 'start'
        self.settings_manager = SettingsManager()
        self.fs_path = self.settings_manager.get_paths()[FilePath.FS]
        self.java_pid_file_path = self.settings_manager.get_QTHZ_inst_path()+"\\pid.txt"
        self.qthz_start_exe = self.settings_manager.get_QTHZ_inst_path()+"\\start.exe"

    def isFreeSwitchRunning(self):
        try:
            process = len(os.popen(
                "tasklist | findstr " + FREESWITCH_PROCESS_NAME
            ).readlines())
        except Exception:
            raise
        else:
            return 1 if process >= 1 else 0
              
    
    def freeswith_call_status(self):
        try:
            self.isFreeSwitchRunning()
        except subprocess.CalledProcessError:
            return None
        try:
            proc = subprocess.check_output(
                ['C:\\Program Files\\FreeSWITCH\\fs_cli.exe', '-x', 'show calls'],
                shell=True,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            #print('sofia status returned nothing')
            return None
        call_num = ""
        if proc != 0:
            result = proc.decode('utf-8')
            result_list = result.split(' ')
            result_list_final = []
            for i in result_list:
                if i == '':
                    pass
                else:
                    result_list_final.append(i)
            call_num_list = result_list_final[-2].split('\t')
            call_num = call_num_list[0]
        return call_num[-1]
        
    
    def freeswitchStatus(self):
        try:
            self.isFreeSwitchRunning()
        except subprocess.CalledProcessError:
            return None
        try:
            proc = subprocess.check_output(
                ['C:\\Program Files\\FreeSWITCH\\fs_cli.exe', '-x', 'sofia status'],
                shell=True,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            #print('sofia status returned nothing')
            return {'reg_numconvert':'unknown', 'reg_callbox': 'unknown'}
        # proc.communicate()
        remote_fs_conn_status = ''
        callbox_conn_status = ''
        if proc != 0:
            result = proc.decode('utf-8')
            result_list = result.split(' ')
            result_list_final = []
            for i in result_list:
                if i == '':
                    pass
                else:
                    result_list_final.append(i)
            for i in result_list_final:
                if i == 'external::numconvert\tgateway\t':
                    remote_fs_conn_status = result_list_final[result_list_final.index(i) + 1]
                elif i == 'external::callbox\tgateway\t':
                    callbox_conn_status = result_list_final[result_list_final.index(i) + 1]
        remote_fs_conn_status_list = remote_fs_conn_status.split('\t')
        callbox_conn_status_list = callbox_conn_status.split('\t')
        return {'reg_numconvert':remote_fs_conn_status_list[-1][:-2], 'reg_callbox': callbox_conn_status_list[-1][:-2]}
    
    def reloadFreeswitch(self):
        '''
        该函数是重新加载fs配置文件
        输入：
        输出：fs重新加载的输出日志
        '''
        try:
            proc = subprocess.check_output([f'{self.fs_path}\\fs_cli.exe', '-x', 'reload mod_sofia'], shell = True, stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.logger.warn('reload mod_sofia returned nothing')
            return 
        else:
            self.logger.info(proc.decode('utf-8'))

    def stopFreeswitch(self):
        '''
        该函数是重关闭fs
        输入：
        输出：
        '''
        try:
            proc = subprocess.check_output([f'{self.fs_path}\\fs_cli.exe', '-x', 'shutdown'], shell = True, stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.logger.warn("fs_cli -x shutdown returned nothing")
            return 0
        else:
            try:
                result = self.isFreeSwitchRunning()
            except subprocess.CalledProcessError:
                self.logger.info("fs console not stopped")
                return 0
            else:
                self.logger.info("fs console stopped")
                return 1

    def startFreeswitch(self):
        try:
            proc = subprocess.Popen([f'{self.fs_path}\\FreeSwitchConsole.exe', '-nc'], creationflags=subprocess.DETACHED_PROCESS)
        except Exception:
            self.logger.error(traceback.format_exc())
            return 0
        else:
            try:
                flag = self.isFreeSwitchRunning()

            except subprocess.CalledProcessError:
                self.logger.info("fs is stopped")
            else:
                self.logger.info(f"fs is {'running' if flag else 'stopped'}")
                # print(proc.decode('utf-8'))
                return 1

    def start_QTHZ(self):
        self.logger.info("启动前置服务")
        try:
            proc = subprocess.Popen([self.qthz_start_exe], creationflags=subprocess.DETACHED_PROCESS)
        except Exception:
            self.logger.error(traceback.format_exc())
            return 0

    def stop_java(self):
        self.logger.info("停止JAVA")
        pid = self.isJavaRunning()
        if(pid):
            try:
                p = psutil.Process(int(pid))
                p.terminate()
            except Exception:
                return 0
            else:
                return 0

    def isJavaRunning(self):
        try:
            with open(self.java_pid_file_path, 'r') as pid_file:
                self.logger.debug("读取PID文件")
                java_pid = pid_file.read().strip()
                exists = psutil.pid_exists(int(java_pid))
        except FileNotFoundError:
            self.logger.debug("PID文件不存在")
            return 0
        except Exception:
            self.logger.debug("JAVA不在运行")
            return 0
        else:
            self.logger.debug("Java正在运行, PID: %s", java_pid)
            return java_pid if exists else 0
    
    def keepFsAlive(self):
        if self.isFreeSwitchRunning():
            return None
        else:
            try:
                os.system('"C:\\Program Files\\FreeSWITCH\\FreeSwitchConsole.exe" -nc')
            except Exception:
                print(traceback.format_exc())
                return 0
            else:
                try:
                    self.isRunning(FREESWITCH_PROCESS_NAME)
                
                except subprocess.CalledProcessError:
                    #print("fs is stopped")
                    raise
                else:
                    return 1
            
    def keepJavaAlive(self):
        if self.isJavaRunning():
            return None
        else:
            #TODO
            #添加Java的启动脚本
            print()

    
    
    
        