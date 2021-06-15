import os
import subprocess
import traceback

FREESWITCH_PROCESS_NAME = 'FreeSwitch'
JAVA_PROCESS_PORT = '18080'

class getProcessStatus:
	def __init__(self):
		start = 'start'
	
	def isFreeSwitchRunning(self):
		try:
			process = len(os.popen(
				"tasklist | findstr " + FREESWITCH_PROCESS_NAME
			).readlines())
		except Exception:
			raise
		else:
			if process >= 1:
				fs_flag =  True
			else:
				fs_flag = False
			return fs_flag
	
	def freeswith_call_status(self):
		try:
			self.isFreeSwitchRunning()
		except subprocess.CalledProcessError:
			return None
		try:
			proc = subprocess.check_output(
				['C:\\Program Files\\FreeSWITCH\\fs_cli.exe', '-x', 'show calls'],
				shell=True,
				stdin=subprocess.DEVNULL,
				stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError:
			#print('sofia status returned nothing')
			return None
		call_num = ""
		if proc != 0:
			result = proc.decode('utf-8')
			result_list = result.split(' ')
			result_list_final = []
			for i in result_list:
				if i == '':
					pass
				else:
					result_list_final.append(i)
			call_num_list = result_list_final[-2].split('\t')
			call_num = call_num_list[0]
		return call_num[-1]
		
	
	def freeswitchStatus(self):
		try:
			self.isFreeSwitchRunning()
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
			return {'reg_numconvert':'unknown', 'reg_callbox': 'unknown'}
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
		return {'reg_numconvert':remote_fs_conn_status_list[-1][:-2], 'reg_callbox': callbox_conn_status_list[-1][:-2]}
	
	def isJavaRunning(self):
		try:
			process = len(os.popen(
				"netstat | findstr " + JAVA_PROCESS_PORT
			).readlines())
		except Exception:
			pass
		else:
			if process >= 1:
				return True
			else:
				return False
	
	def keepFsAlive(self):
		if self.isFreeSwitchRunning():
			return None
		else:
			try:
				os.system('"C:\\Program Files\\FreeSWITCH\\FreeSwitchConsole.exe" -nc')
			except Exception:
				print(traceback.format_exc())
				return 0
			else:
				try:
					self.isRunning(FREESWITCH_PROCESS_NAME)
				
				except subprocess.CalledProcessError:
					#print("fs is stopped")
					raise
				else:
					return 1
			
	def keepJavaAlive(self):
		if self.isJavaRunning():
			return None
		else:
			#TODO
			#添加Java的启动脚本
			print()

	
	
	
		