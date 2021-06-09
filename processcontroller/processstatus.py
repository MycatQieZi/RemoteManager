import os
import sys
import traceback
import time
import subprocess
# import psutil

FREESWITCH_PROCESS_NAME = 'FreeSwitch'
JAVA_PROCESS_NAME = 'java'

class getProcessStatus:
	def __init__(self):
		self.REG_CALLBOX, self.REG_NUMCONVERT = self.freeswitchStatus()
	
	def isRunning(self, process_name):
		try:
			process = len(subprocess.check_output(
				["tasklist", "|", "findstr", process_name],
				shell = True,
				stdin = subprocess.DEVNULL,
				stderr = subprocess.STDOUT
			))
		except subprocess.CalledProcessError:
			raise
		except Exception:
			raise
		else:
			if process >= 1:
				return True
			else:
				return False
	
	def freeswitchStatus(self):
		'''
		该函数是用来查看本地fs的双向注册状态，即为callbox的注册状态和numconvert的注册状态
		输入：
		输出：<str>callbox注册状态，<str>numconvert注册状态
		'''
		try:
			self.isRunning(FREESWITCH_PROCESS_NAME)
		except subprocess.CalledProcessError:
			return None
		try:
			proc = subprocess.check_output(
				['C:\\Program Files\\FreeSWITCH\\fs_cli.exe', '-x', 'sofia status'],
				shell=True,
				stdin=subprocess.DEVNULL,
				stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError:
			#print('sofia status returned nothing')
			return None
		# proc.communicate()
		remote_fs_conn_status = ''
		callbox_conn_status = ''
		if proc != 0:
			result = proc.decode('utf-8')
			result_list = result.split(' ')
			result_list_final = []
			for i in result_list:
				if i == '':
					pass
				else:
					result_list_final.append(i)
			for i in result_list_final:
				if i == 'external::numconvert\tgateway\t':
					remote_fs_conn_status = result_list_final[result_list_final.index(i) + 1]
				elif i == 'external::callbox\tgateway\t':
					callbox_conn_status = result_list_final[result_list_final.index(i) + 1]
		remote_fs_conn_status_list = remote_fs_conn_status.split('\t')
		callbox_conn_status_list = callbox_conn_status.split('\t')
		return remote_fs_conn_status_list[-1][:-2], callbox_conn_status_list[-1][:-2]
	
	def isJavaRunning(self):
		if self.isRunning(JAVA_PROCESS_NAME):
		
	