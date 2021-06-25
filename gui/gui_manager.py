from misc.decorators import singleton
from utils.my_logger import logger
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from gui.sys_tray import SysTray
from scheduler.lock_manager import LockManager

import traceback, threading, time

@singleton
@logger
class GUIManager():
    def __init__(self, **fns):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(True)

        self.getUserTokenThread = None
        self.getVersionCheckThread = None
        self.updateConfigThread = None
        self.sendHeartbeatThread = None
        self.clearCacheThread = None
        self.installUpdateThread = None
        self.threads = [
            self.getUserTokenThread,
            self.getVersionCheckThread,
            self.updateConfigThread,
            self.sendHeartbeatThread,
            self.clearCacheThread,
            self.installUpdateThread
        ]

        self.parent_exit = fns['safeExit']
        
        # TODO: refactor 
        self.sysTray = SysTray(
            self.app, 
            getUserToken=lambda: self.onClickGetUserToken(fns['getUserToken']),
            getVersionCheck=lambda: self.onClickGetVersionCheck(fns['getVersionCheck']),
            updateConfig=lambda: self.onClickUpdateConfig(fns['updateConfig']),
            sendHeartbeat=lambda: self.onClickSendHeartbeat(fns['sendHeartbeat']),
            clearCache=lambda: self.onClickClearCache(fns['clearCache']),
            installUpdate=lambda: self.onClickInstall(fns['installUpdate']),
            safeExit=self.onClickSafeExit
            )
        
        # self.app.exec_()

    def onClickGetUserToken(self, getUserToken):
        if self.getUserTokenThread and self.getUserTokenThread.is_alive():
            return 
    
        self.getUserTokenThread = threading.Thread(target=getUserToken, name="GetTokenThread")
        self.getUserTokenThread.start()
        
    def onClickGetVersionCheck(self, getVersionCheck):
        if self.getVersionCheckThread and self.getVersionCheckThread.is_alive():
            return 
        self.getVersionCheckThread = threading.Thread(target=getVersionCheck, name='VersionCheckThread')
        self.getVersionCheckThread.start()

    def onClickUpdateConfig(self, updateConfig):
        if self.updateConfigThread and self.updateConfigThread.is_alive():
            return 

        self.updateConfigThread = threading.Thread(target=updateConfig, name='UpdateConfigThread')
        self.updateConfigThread.start() 

    def onClickSendHeartbeat(self, sendHeartbeat):
        if self.sendHeartbeatThread and self.sendHeartbeatThread.is_alive():
            return
        
        self.sendHeartbeatThread = threading.Thread(target=sendHeartbeat, name='HeartbeatThread')
        self.sendHeartbeatThread.start()

    def onClickClearCache(self, clearCache):
        if self.clearCacheThread and self.clearCacheThread.is_alive():
            return
        
        self.clearCacheThread = threading.Thread(target=clearCache, name='ClearCacheThread')
        self.clearCacheThread.start()

    def onClickInstall(self, installUpdate):
        if self.installUpdateThread and self.installUpdateThread.is_alive():
            return
        
        self.installUpdateThread = threading.Thread(target=installUpdate, name='InstallatonThread')
        self.installUpdateThread.start()

    def onClickSafeExit(self, fn_systray_exit):
        self.parent_exit(self.clean_up_threads)
        # time.sleep(10)
        fn_systray_exit()

    def clean_up_threads(self):
        for thread in self.threads:
            if thread:
                self.logger.debug('join: ', thread)
                thread.join()
        self.logger.debug("准备退出, 等待线程结束...")
        time.sleep(3)

if __name__ == '__main__':
    g = GUIManager()
