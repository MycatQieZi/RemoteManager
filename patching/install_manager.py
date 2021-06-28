from processcontroller.processstatus import ProcessManager
from conf.config import ConfigManager
from scheduler.lock_manager import LockManager
from misc.enumerators import FilePath, PatchCyclePhase, PatchStatus
from patching.patch_manager import PatchManager
from settings.settings_manager import SettingsManager
from misc.decorators import singleton, with_lock
from utils.my_logger import logger
from pathlib import Path
from os import listdir
from os.path import isfile, join, exists
import shutil, traceback, time, sqlite3, threading

@singleton
@logger
class InstallManager:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.patch_manager = PatchManager()
        self.lock_manager = LockManager()
        self.config_manager = ConfigManager()
        self.process_manager = ProcessManager()
        self.install_update_lock = self.lock_manager.install_update_lock 
        self.heartbeat_lock = self.lock_manager.heartbeat_lock
    
    def clear_download_cache(self):
        self.logger.info("清除下载缓存")
        patch_dir = self.settings_manager.get_patch_dir_path()
        try:
            shutil.rmtree(patch_dir)
        except:
            self.logger.debug("清除失败")
        else:
            self.logger.info("清除完毕")

    def install_update(self):
        @with_lock(self.install_update_lock, logger=self.logger)
        @with_lock(self.heartbeat_lock, blocking=True, logger=self.logger)
        def installation_driver():
            self.patch_manager.load_meta()
            # extra try-catch block to ensure a lock-release when @with_lock decorator finishes execution
            try: 
                if(self.patch_manager.state < PatchCyclePhase.PENDING 
                    or self.patch_manager.state > PatchCyclePhase.PREPPED):
                    self.logger.info("暂无需要安装的更新")
                    return 1
                self.pause_all_operations()
                self.logger.info("开始安装更新")
                result = self.installation()
            except Exception:
                return 0
            else:
                return result
        try:    
            result = installation_driver()
        except Exception as e:
            self.logger.error(traceback.format_exc())
            result = 0
        finally:
            self.logger.debug("安装流程: %s", '完成' if result else '异常') 
        
    def installation(self):
        if self.patch_manager.state == PatchCyclePhase.PENDING:
            result = self.create_backup()
        if self.patch_manager.state == PatchCyclePhase.PREPPED:
            result = self.replace_files()
        if self.patch_manager.state == PatchCyclePhase.COMPLETE:
            result = self.post_installation_cleanup()
        if self.patch_manager.state == PatchCyclePhase.ROLLEDBACK:
            # TODO: do something to mitigate the aftermath
            self.patch_manager.state = PatchCyclePhase.PENDING
            for index, _ in enumerate(self.patch_manager.patch_objs):
                patch_obj = self.patch_manager.patch_objs[index]
                patch_obj.status = PatchStatus.DOWNLOADED
            self.patch_manager.dump_meta()
            self.logger.info("可尝试再次安装")
        self.resume_all_operations()
        return result

    def create_backup(self):
        try:
            self.logger.info("文件备份中")
            backup_dir = self.settings_manager.get_backup_dir_path()
            Path(backup_dir).mkdir(parents=True, exist_ok=True)
            db_dir = self.settings_manager.get_sqlite_db_path()
            shutil.copytree(db_dir, backup_dir+"/data", dirs_exist_ok=True)
            jar_path = self.settings_manager.get_QTHZ_inst_path()+"/icb-box.jar"
            shutil.copy2(jar_path, backup_dir)
            conf_path = self.settings_manager.get_paths()[FilePath.CONFIG]
            shutil.copy2(conf_path, backup_dir)
            self.logger.info("文件备份完毕")    
        except Exception:
            self.logger.error(traceback.format_exc())
            raise
        else:
            self.patch_manager.state = PatchCyclePhase.PREPPED
            self.patch_manager.dump_meta()
            return 1

    def revert_backup(self, patch_objs):
        self.patch_manager.state = PatchCyclePhase.ROLLEDBACK
        for index, _ in enumerate(patch_objs):
            patch_obj = patch_objs[index]
            patch_obj.status = PatchStatus.REVERTED
            self.logger.debug("记录回滚版本: %s", patch_obj.version_num)
        self.revert_to_last()
        self.patch_manager.dump_meta()
        self.logger.info("回滚完成")

    def revert_to_last(self):
        backup_dir = self.settings_manager.get_backup_dir_path()
        db_dir = self.settings_manager.get_sqlite_db_path()
        shutil.rmtree(db_dir)
        shutil.copytree(backup_dir+"/data", db_dir, dirs_exist_ok=True)
        qthz_path = self.settings_manager.get_QTHZ_inst_path()
        shutil.copy2(backup_dir+"\\icb-box.jar", qthz_path)
        shutil.copy2(backup_dir+"\\configuration.ini", qthz_path+"\\conf")
        self.config_manager.load_config()
        self.logger.info("文件回滚完毕")

    def replace_files(self):
        self.logger.debug("开始文件更替")
        patch_objs = self.patch_manager.patch_objs
        for index, patch_obj in enumerate(patch_objs):
            if not patch_obj.status == PatchStatus.DOWNLOADED:
                continue
            try:
                self.replace_one_version(patch_objs[index])
            except Exception as e_outer: # any exception or error, will trigger a rollback
                self.logger.error("安装流程出现异常, 回滚中: %s", traceback.format_exc())
                try:
                    self.revert_backup(patch_objs)
                except Exception as e_inner:
                    self.logger.error("回滚失败 %s", traceback.format_exc())
                    raise e_inner
                else:
                    return 0
            
            else: # 
                # change patch_obj PatchStatus
                patch_objs[index].status = PatchStatus.INSTALLED
                self.logger.debug("完成一个版本的安装: %s", patch_obj.version_num)
        self.patch_manager.state = PatchCyclePhase.COMPLETE
        self.patch_manager.dump_meta()
        self.logger.info("遍历安装完成")
        return 1

    def replace_one_version(self, patch_obj):
        arg_conf_map = patch_obj.argument_config_map
        version_num = patch_obj.version_num
        version_code = patch_obj.version_code
        patch_dir_path = "%s\\%s" %(self.settings_manager.get_patch_dir_path(),version_num)
        qthz_path = self.settings_manager.get_QTHZ_inst_path()
        
        self.logger.info("开始安装版本: %s", version_num)
        # TODO: update RemoteManager
        # TODO: execute sh commands 
        
        # exec sql script; or replace sqlite source file 
        self.update_sqlite_db(patch_dir_path, qthz_path, arg_conf_map)

        # TODO: replace JAR
        jar_patch = patch_dir_path+"\\icb-box.jar"
        if exists(jar_patch):
            shutil.copy2(jar_patch, qthz_path)
            self.logger.debug("更替JAR包完成")

        # TODO: replace lua scripts
        
        # overwrite configuration.ini
        self.config_manager.update_remote_config(arg_conf_map, patch_obj.version_num, patch_obj.version_code)
    
    def update_sqlite_db(self, patch_dir_path, qthz_path, arg_conf_map):
        db_patch_dir = patch_dir_path+"\\data"
        db_dir = qthz_path+"\\data"
        sqlite_file = None
        sql_script = None
        dotdb_file = None
        # if the '/data' dir exists in patch_dir, theres a need to update data
        should_update_data = exists(db_patch_dir)
        if should_update_data:
            self.logger.debug("需要更新SQL数据")
            onlyfiles = [f for f in listdir(db_patch_dir) if isfile(join(db_patch_dir, f))]
            for file in onlyfiles:
                parts = file.split('.')
                if len(parts)<2:
                    sqlite_file = file
                else:
                    if parts[1]=='sql':
                        sql_script = file
                    elif parts[1]=='db':
                        dotdb_file = file
        
        # if there exists a sql script to be exec-ed, 
        if(sql_script):
            self.logger.debug("需要执行SQL命令")
            # find the old sqlite db source,
            old_sqlite_file = None
            onlyfiles = [f for f in listdir(db_dir) if isfile(join(db_dir, f))]
            for file in onlyfiles:
                parts = file.split('.')
                if len(parts)<2:
                    old_sqlite_file = file

            # connect to it and execute sql on it
            connection = sqlite3.connect(db_dir+"\\"+old_sqlite_file)
            cursor = connection.cursor()
            with open(db_patch_dir+"\\"+sql_script, 'r', encoding='utf-8') as sql_file:
                sql_as_string = sql_file.read()
                try:
                    cursor.executescript(sql_as_string)
                except Exception:
                    cursor.execute('rollback')
                    self.logger.error("SQL命令执行异常: %s", traceback.format_exc())
                    raise
                finally:
                    connection.close()
                self.logger.debug("SQL命令完毕")

        # copy all files from patch dir to data dir
        if should_update_data:
            shutil.copytree(db_patch_dir, db_dir, dirs_exist_ok=True)

        # if theres a need to mount a new sqlite db source
        # save the filename to config.ini
        if(sqlite_file):
            self.logger.debug("需要修改挂载的SQLite数据库源文件")
            arg_conf_map['dbfileName'] = sqlite_file

        self.logger.debug("数据更新完成")

    def post_installation_cleanup(self):
        self.patch_manager.state = PatchCyclePhase.READY
        self.patch_manager.dump_meta()
        self.config_manager.load_config()
        self.config_manager.save_fs_conf()
        self.logger.info("安装更新完成!")
        return 1

    def pause_all_operations(self):
        self.logger.debug("Halting all operations, triggering killswitch in...")
        # fs_stopper_thread = threading.Thread(target=self.process_manager.stopFreeswitch)
        # fs_stopper_thread.start() 
        # java_stopper_thread = threading.Thread(target=self.process_manager.stop_java)
        # java_stopper_thread.start()
        self.process_manager.stopFreeswitch()
        self.process_manager.stop_java()
        # countdown = 3
        # for i in range(countdown, 0, -1):
        #     self.logger.debug(i)
        #     time.sleep(1)
        # fs_stopper_thread.join()
        # java_stopper_thread.join()
        

    def resume_all_operations(self):
        self.logger.info("Resuming operations immediately!")
        starter_thread =  threading.Thread(target=self.process_manager.start_QTHZ)
        starter_thread.start()
        self.config_manager.load_config()
        starter_thread.join()

    


