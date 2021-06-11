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
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        
        # Creating the options
        menu = QMenu()
        option1 = QAction("GET user Token")
        option1.triggered.connect(fns['getUserToken'])
        option2 = QAction("GET version check")
        option2.triggered.connect(fns['getVersionCheck'])
        menu.addAction(option1)
        menu.addAction(option2)
        
        # To quit the app
        quit = QAction("Quit")
        quit.triggered.connect(self.app.quit)
        menu.addAction(quit)
        
        # Adding options to the System Tray
        tray.setContextMenu(menu)
        self.app.exec_()

    
