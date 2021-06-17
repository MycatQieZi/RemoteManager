from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from gui.sys_tray import SysTray
from utils.my_logger import logger

import traceback

@logger
class GUIManager():
    def __init__(self, **fns):
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
            self.error(traceback.format_exc())


    def onClickGetVersionCheck(self, getVersionCheck):
        
        try:
            content = getVersionCheck()
        except Exception as e:
            self.error(traceback.format_exc())
        else:
            self.debug("GET version check: %s", str(content))
        

if __name__ == '__main__':
    g = GUIManager()
