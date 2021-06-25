from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import pathlib

class SysTray():
    def __init__(self, app, **fns):
        self.app = app
        
        curr_script_path = pathlib.Path(__file__).parent.absolute()
        # Adding an icon
        icon = QIcon(str(curr_script_path)+"/tool-box-64.ico")
        
        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setToolTip("智能盒子运维管理")
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        
        # Creating the options
        menu = QMenu()
        self.update_menu = menu.addMenu("更新")
        self.debug_menu = menu.addMenu("调试")
        update_actions = [
            {'title': '检查更新', 'fn': 'getVersionCheck'},
            {'title': '清除缓存', 'fn': 'clearCache'},
            {'title': '安装更新', 'fn': 'installUpdate'}
        ]
        for action in update_actions:
            option = QAction(action['title'], self.app)
            option.triggered.connect(fns[action['fn']])
            self.update_menu.addAction(option)
        
        debug_actions = [
            {'title': '获取口令', 'fn': 'getUserToken'},
            {'title': '重载配置', 'fn': 'updateConfig'},
            {'title': '心跳发送', 'fn': 'sendHeartbeat'}
        ]
        for action in debug_actions:
            option = QAction(action['title'], self.app)
            option.triggered.connect(fns[action['fn']])
            self.debug_menu.addAction(option)
        
        # To quit the app
        quit = QAction("退出")
        quit.triggered.connect(lambda: fns['safeExit'](self.exit_gracefully))
        menu.addAction(quit)
        
        # Adding options to the System Tray
        self.tray.setContextMenu(menu)
        self.app.exec_()

    def exit_gracefully(self):
        print("退出")
        self.app.quit()
    
