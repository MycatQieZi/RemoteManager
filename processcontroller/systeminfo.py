import psutil
import time
import datetime
import uuid
import socket

class getSystemInfo:
	def __init__(self):
		start = "start"

	def cpu_rate(self):
		cpu_status = psutil.cpu_percent(1)
		return str(cpu_status)
	
	def users(self):
		user_str = ""
		user_status = psutil.users()
		for item in user_status:
			user_str += str(item)
		return user_str
	
	def mac_name_ip(self):
		''' 获得Mac地址、计算机名、IP地址 '''
		mac = uuid.UUID(int=uuid.getnode()).hex[-12:]  # Mac地址
		name = socket.getfqdn(socket.gethostname())  # 计算机名称
		addr = socket.gethostbyname(name)  # IP地址
		return {'mac':mac, 'name':name, 'addr':addr}
	
	def mem_rate(self):
		# 本机内存的占用率
		return psutil.virtual_memory().percent