import socket
import win32serviceutil
import servicemanager
import win32event
import win32service

class SMWinservice(win32serviceutil.ServiceFramework):
    #服务名
    _svc_name_ = 'RemoteControllerService'
    #服务在windows系统中显示的名称
    _svc_display_name_ = 'RemoteControllerService'
    #服务描述
    _svc_description_ = '智能盒子远程控制客户端'
    # @classmethod
    # def parse_command_line(cls):
    #     '''
    #     ClassMethod to parse the command line
    #     '''
    #     win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.run = True

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        '''
        Main class to be ovverridden to add logic
        '''
        pass

# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    SMWinservice.parse_command_line()