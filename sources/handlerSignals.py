# Author: Ivan Heredia Planas
# 2 CFGS ASIX
#
# This HandlerSignals class is used at close the client (ClassAdmin.socket) or (ClassAdminS.socket)
#
import signal, platform
class HandlerSignals:
    def __init__(self,sock):
        self.sock = sock
        #shutdown signal in Linux
        signal.signal(signal.SIGTERM,self.shutdown)
        # shutdown signal in Windows
        if platform.system().upper()=="WINDOWS":
            import win32api
            win32api.SetConsoleCtrlHandler(self.shutdownWin, True)

    def shutdownWin(self,a):
        self.sock.close()

    def shutdown(self,code,msg):
        raise SystemExit

