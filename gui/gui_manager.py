from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from base_manager import BaseManager
from gui.sys_tray import SysTray
import traceback

class GUIManager(BaseManager):
    def __init__(self, env, **fns):
        super().__init__(env)
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)

        
        self.sysTray = SysTray(
            self.app, 
            getUserToken = lambda: self.onClickGetUserToken(fns['getUserToken']),
            getVersionCheck = lambda: self.onClickGetVersionCheck(fns['getVersionCheck']))
        
        # self.app.exec_()

    def onClickGetUserToken(self, getUserToken):
        try:
            getUserToken()
        except Exception as e:
            self.logger.error(traceback.format_exc())


    def onClickGetVersionCheck(self, getVersionCheck):
        
        try:
            content = getVersionCheck()
        except Exception as e:
            self.logger.error(traceback.format_exc())
        else:
            self.logger.debug("GET version check: %s", str(content))
        

if __name__ == '__main__':
    g = GUIManager()
