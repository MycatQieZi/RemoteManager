from winreg import *

"""
demo to get Qthz installation path in registry
TODO: replace as a generic reg_reading method
""" 

REG_PATH = "SOFTWARE\\Ect888\\Qthz"
INSTALL_PATH_KEY = "QthzInstallPath"

RUN_ON_STARTUP_PATH = "\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"

def reg_get_QTHZ_path():
	try:
		reg = OpenKey(HKEY_LOCAL_MACHINE, REG_PATH)
		path = QueryValueEx(reg, INSTALL_PATH_KEY)
		# print("path: ",path[0])
		return path[0];
	except EnvironmentError as e:
		print(e)    
	