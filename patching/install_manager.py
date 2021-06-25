from conf.config import ConfigManager
from scheduler.lock_manager import LockManager
from misc.enumerators import FilePath, PatchCyclePhase, PatchStatus
from patching.patch_manager import PatchManager
from settings.settings_manager import SettingsManager
from misc.decorators import singleton, with_lock
from utils.my_logger import logger
from pathlib import Path
import shutil, traceback, os, time

@singleton
@logger
class InstallManager:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.patch_manager = PatchManager()
        self.lock_manager = LockManager()
        self.config_manager = ConfigManager()
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
            if(self.patch_manager.state < PatchCyclePhase.PENDING 
                or self.patch_manager.state > PatchCyclePhase.PREPPED):
                self.logger.info("暂无需要安装的更新")
                return 1
            
            self.logger.info("开始安装更新")
            return self.installation()
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
            self.logger.debug("完事儿了")
            result = self.post_installation_cleanup()
        if self.patch_manager.state == PatchCyclePhase.ROLLEDBACK:
            # TODO: maybe clean up download?
            pass

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
            return 0
        else:
            self.patch_manager.state = PatchCyclePhase.PREPPED
            self.patch_manager.dump_meta()
            return 1

    def revert_backup(self, patch_objs):
        # TODO: WIP
        self.patch_manager.state = PatchCyclePhase.ROLLEDBACK
        for index, _ in enumerate(patch_objs):
            patch_obj = patch_objs[index]
            patch_obj.status = PatchStatus.REVERTED
            self.logger.debug("回滚版本: %s", patch_obj.version_num)
            backup_dir = self.settings_manager.get_backup_dir_path()
            db_dir = self.settings_manager.get_sqlite_db_path()
            shutil.copytree(backup_dir+"/data", db_dir, dirs_exist_ok=True)
            qthz_path = self.settings_manager.get_QTHZ_inst_path()
            shutil.copy2(backup_dir+"\\icb-box.jar", qthz_path)
            shutil.copy2(backup_dir+"\\configuration.ini", qthz_path+"\\conf")
            self.logger.info("文件回滚完毕")
        self.patch_manager.dump_meta()
        self.logger.info("回滚完成")

    def replace_files(self):
        self.logger.debug("开始文件更替")
        patch_objs = self.patch_manager.patch_objs
        for index, patch_obj in enumerate(patch_objs):
            if not patch_obj.status == PatchStatus.DOWNLOADED:
                continue
            try:
                self.replace_one_version(patch_objs[index])
            except: # any exception or error, will trigger a rollback
                self.logger.error("安装流程出现异常, 回滚中: %s", traceback.format_exc())
                self.revert_backup(patch_objs)
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
        # TODO: update RemoteManager
        # TODO: execute sh commands 
        # TODO: run sql 
        # TODO: replace JAR
        # TODO: replace lua scripts
        
        # overwrite configuration.ini
        arg_conf_map = patch_obj.argument_config_map
        self.config_manager.update_remote_config(arg_conf_map, patch_obj.version_num, patch_obj.version_code)
        
    def post_installation_cleanup(self):
        #self.patch_manager.state = PatchCyclePhase.READY
        self.patch_manager.dump_meta()
        self.logger.info("安装更新完成!")
        self.config_manager.load_config()
        return 1

    def pause_all_operations(self):
        self.logger.info("ALL STATION, ALL STATION, halt all operations immediately! Triggering killswitch in...")
        countdown = 5
        for i in range(countdown, 0, -1):
            self.logger.info(i)
            time.sleep(1)
        

    def resume_all_operations(self):
        self.config_manager.load_config()
        self.logger.info("ALL STATION, ALL STATION, resume operations immediately!")

    


