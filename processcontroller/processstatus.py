from gui.winrt_toaster import toast_notification
from misc.enumerators import FilePath
from settings.settings_manager import SettingsManager
from utils.my_logger import logger
from misc.decorators import singleton
import os
import subprocess
import traceback
import psutil
import time
import webbrowser

FREESWITCH_PROCESS_NAME = 'FreeSwitch'
JAVA_PROCESS_PORT = '18080'
ICB_BOX_JAVA__PROC_NAME = 'java'

@singleton
@logger
class ProcessManager:
    def __init__(self):
        start = 'start'
        self.settings_manager = SettingsManager()
        paths = self.settings_manager.get_paths()
        self.fs_path = paths[FilePath.FS]
        self.qthz_path = self.settings_manager.get_QTHZ_inst_path()
        self.java_pid_file_path = paths[FilePath.JAVA_PID]
        self.yaml_path = paths[FilePath.APP_YML]
        self.config_path = paths[FilePath.CONFIG]
        self.batch_file = paths[FilePath.PATH_BAT]
        self.jar_path = paths[FilePath.JAR]

    def start_QTHZ(self):
        self.logger.info("启动前置服务")
        toast_notification("证通智能精灵", "正在启动", "正在启动智能精灵")
        try:
            self.update_jar_app_yaml()
            self.start_reload_freeswitch()
            self.start_reload_java()
            time.sleep(10)
            webbrowser.open("http://127.0.0.1:18080")
        except Exception:
            self.logger.error(traceback.format_exc())
            return 0
    
    def open_qthz(self):
        # 和 start_QTHZ 有区别
        self.logger.info("启动前置服务")
        toast_notification("证通智能精灵", "正在开启", "正在打开智能精灵管理平台")
        if not self.is_freeswitch_running():
            self.start_freeswitch()
        if not self.is_java_running():
            self.start_java()
            time.sleep(10)
        
        webbrowser.open("http://127.0.0.1:18080")

# ========================= FREESWITCH management++++++++++++++++ 

    def is_freeswitch_running(self):
        try:
            process = subprocess.check_output(
                ["tasklist", "|", "findstr", FREESWITCH_PROCESS_NAME],
                shell=True,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            self.logger.info("fs is stopped")
            return 0
        else:
            return 1 if len(process) >= 1 else 0
              
    
    def freeswith_call_status(self):
        status = self.is_freeswitch_running()
        if not status:
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
        
    
    def freeswitch_status(self):
        status = self.is_freeswitch_running()
        if not status:
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
    
    def reload_freeswitch(self):
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

    def stop_freeswitch(self):
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
            result = self.is_freeswitch_running()
            self.logger.info(f"FS {'仍在运行' if result else '已经终止'}")
            return result

    def start_reload_freeswitch(self):
        if self.is_freeswitch_running():
            self.logger.info("FS已经启动, 需要重启以应用新配置")
            self.reload_freeswitch()
            return 1
        return self.start_freeswitch()

    def start_freeswitch(self):
        try:
            proc = subprocess.Popen([f'{self.fs_path}\\FreeSwitchConsole.exe', '-nc'], creationflags=subprocess.DETACHED_PROCESS)
        except Exception:
            self.logger.error(traceback.format_exc())
            return 0
        else:
            self.logger.info("FS启动成功, pid: %s", proc.pid)
            return 1

    def keep_fs_alive(self):
        if self.is_freeswitch_running():
            return None
        else:
            try:
                self.start_freeswitch()
                self.logger.info("FS守护检测到FS进程已停止, 正在重启")
            except Exception:
                print(traceback.format_exc())
                return 0

# -------------------- JAVA management ----------------------
    def is_java_running(self):
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
            self.logger.debug(f"Java{'正在运行' if exists else '未启动'}, PID: %s", java_pid)
            return java_pid if exists else 0
    

    def stop_java(self):
        pid = self.is_java_running()
        if not pid:
            return 0
        try:
            p = psutil.Process(int(pid))
            p.terminate()
        except Exception:
            self.logger.info("未能停止JAVA")
            return 0
        else:
            self.logger.info("停止JAVA")
            return 1

    
    def start_reload_java(self):
        self.logger.info('启动java')
        self.stop_java()
        self.set_java_env()
        return self.start_java()

    def start_java(self):
        try:
            # popen 用列表传参数
            order = ['java', '-jar', self.jar_path, f'--spring.config.location={self.yaml_path}']
            proc = subprocess.Popen(order, shell=False, creationflags=subprocess.DETACHED_PROCESS)
            self.update_java_pid(proc.pid)
            self.logger.debug("JAVA已启动, pid: %i", proc.pid)
            return 1
        except:
            self.logger.error(traceback.format_exc())
            return 0
            
    def keep_java_alive(self):
        if(self.is_java_running()):
            return 
        self.logger.info("JAVA守护检测到JAVA进程已停止, 正在重启")
        self.start_java()



    def update_java_pid(self, pid):
        with open(self.java_pid_file_path, "w", encoding="utf-8") as pid_file: 
            pid_file.write(str(pid))


    def set_java_env(self):
        self.logger.debug('添加JAVA环境变量')
        try:
            p = subprocess.Popen(
                ["cmd.exe", "/c", self.batch_file], 
                # shell=True, 
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
        except:
            self.logger.error(traceback.format_exc())
            return 
        curline = p.stdout.readline()
        while (curline != b''):
            #(curline)
            curline = p.stdout.readline()
        p.wait()
        self.logger.info('添加JAVA环境变量完成')
        #print(p.returncode)

    
    def update_jar_app_yaml(self):
        config = self.settings_manager.read_ini_into_config(self.config_path)
        yml_data = self.settings_manager.get_yaml_info(self.yaml_path)
        yml_data['appkey'] = "${APP_KEY:" + config["appkey"]["key"] + "}"
        yml_data['access-key-id'] = "${ACCESS_KEY_ID:" + config["accessid"]["id"] + "}"
        yml_data['access-key-secret'] = "${ACCESS_KEY_SECRET:" + config["accesssecret"]["secret"] + "}"
        yml_data['city-code'] = "${CITY_CODE:" + config["city"]["num"] + "}"
        yml_data['url-port'] = "${ICB-PORT:" + config["host"]["adr"] + "}"
        yml_data['spring']['datasource']['druid']['url'] = f'jdbc:sqlite:{self.qthz_path}\\data\\{config["dbfile"]["name"]}'
        self.settings_manager.write_yaml_info(self.yaml_path, yml_data)
        self.logger.debug("修改JAR包Spring参数")
    
    
    
        