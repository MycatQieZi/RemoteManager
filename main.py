from SMWinservice import SMWinservice

class RemoteManager(SMWinservice):
	_svc_name_ = "RemoteManagerService"
	_svc_display_name_ = "Remote manager tool for callbox"
	_svc_description_ = "designed by zxy, zy:)"
	
	def start(self):
		self.isrunning = True
	def stop(self):
		self.isrunning = False
	def main(self):
		# 此处作为主函数开始执行的入口
		# 注册服务后运行的内容
		while self.isrunning:
			print("start")
if __name__ == '__main__':
	RemoteManager.parse_command_line()