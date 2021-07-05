from utils.my_logger import logger
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import pathlib, sys

@logger
class SysTray():
    def __init__(self, app, **executables):
        self.app = app
        curr_script_path = pathlib.Path(__file__).parent.absolute()
        # Adding an icon
        icon_path = ".\\resources\\fast.ico" if len(sys.argv)<2 or not sys.argv[1]=='debug' else ".\\gui\\resources\\fast.ico"
        icon = QIcon(icon_path)
        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setToolTip("智能精灵运维管理")
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        
        self.logger.info("加载系统托盘菜单")
        # Creating the options
        menu = QMenu()
        self.update_menu = menu.addMenu("更新")
        # self.debug_menu = menu.addMenu("调试")
        update_actions = [
            # {'title': '检查更新', 'fn': 'getVersionCheck'},
            {'title': '安装更新', 'fn': 'installUpdate'},
            {'title': '清除缓存', 'fn': 'clearCache'}
            # {'title': '版本回退', 'fn': 'revertToLast'}
        ]
        # print(fns)
        self.action_execution_list = []
        self.executables = executables
        for index, action in enumerate(update_actions):
            option = QAction(action['title'], self.app)
            
            option.triggered.connect(lambda _, index=index: self.execute_action_by_index(index))
            self.update_menu.addAction(option)
            self.action_execution_list.append(self.executables[action['fn']])
        
        debug_actions = [
            # {'title': '获取口令', 'fn': 'getUserToken'},
            # {'title': '重载配置', 'fn': 'updateConfig'},
            # {'title': '心跳发送', 'fn': 'sendHeartbeat'}
        ]
        # for action in debug_actions:
        #     option = QAction(action['title'], self.app)
        #     option.triggered.connect(fns[action['fn']])
        #     self.debug_menu.addAction(option)
        
        start_qthz_action = QAction("启动精灵")
        start_qthz_action.triggered.connect(executables['startQTHZ'])
        menu.addAction(start_qthz_action)

        # To quit the app
        quit = QAction("退出")
        quit.triggered.connect(lambda: executables['safeExit'](self.exit_gracefully))
        menu.addAction(quit)
        
        # Adding options to the System Tray
        self.tray.setContextMenu(menu)
        self.app.exec_()

    def execute_action_by_index(self, index):
        executable = self.action_execution_list[index]
        fn_threaded_action = executable['fn']
        kwargs = executable['kwargs']
        fn_threaded_action(**kwargs)

    def exit_gracefully(self):
        print("退出")
        self.app.quit()
    
