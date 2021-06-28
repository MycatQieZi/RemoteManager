import sys

from elevate import elevate
from module_manager import entrypoint

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

if not is_admin():
	elevate(show_console=False)

entrypoint()