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
        self.app.setQuitOnLastWindowClosed(False)


        self.getUserTokenThread = None
        self.getVersionCheckThread = None
        self.updateConfigThread = None
        self.sendHeartbeatThread = None
        self.clearCacheThread = None
        self.installUpdateThread = None
        self.threads = {
            'getUserToken': self.getUserTokenThread,
            'getVersionCheck': self.getVersionCheckThread,
            'updateConfig': self.updateConfigThread,
            'sendHeartbeat': self.sendHeartbeatThread,
            'clearCache': self.clearCacheThread,
            'installUpdate': self.installUpdateThread
        }

        self.parent_exit = fns['safeExit']
        
        sys_tray_fn_kwargs = {
            "revertToLast": fns['revertToLast'],
            "startQTHZ": fns['startQTHZ'],
            "safeExit": self.onClickSafeExit
        }
        for key, thread in self.threads.items():
            sys_tray_fn_kwargs[key] = {'fn': self.threaded_execution_wrapper(fns[key]),
                'kwargs': {'thread_instance': thread, 'thread_name': f"{key}Thread"}
            }
        self.sysTray = SysTray(self.app, **sys_tray_fn_kwargs)


    def threaded_execution_wrapper(self, fn_action):
        def inner_wrapper(**kwargs):
            thread_instance = kwargs['thread_instance'] 
            thread_name = kwargs['thread_name']
            if thread_instance and thread_instance.is_alive():
                return 
            thread_instance = threading.Thread(target=fn_action, name=thread_name)
            thread_instance.start()
        return inner_wrapper
    

    def onClickSafeExit(self, fn_systray_exit):
        self.parent_exit(self.clean_up_threads)
        # time.sleep(10)
        fn_systray_exit()

    def clean_up_threads(self):
        for _, thread in self.threads.items():
            if thread:
                self.logger.debug('join: ', thread)
                thread.join()
        self.logger.debug("准备退出, 等待线程结束...")
        time.sleep(3)

if __name__ == '__main__':
    g = GUIManager()
