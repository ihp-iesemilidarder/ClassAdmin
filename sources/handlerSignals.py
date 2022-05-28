# Author: Ivan Heredia Planas
# ivanherediaplanas@protonmail.com
#
# Licensed by GNU GENERAL PUBLIC LICENSE VERSION 3
# This file is part of ClassAdmin.
# ClassAdmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# ClassAdmin is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with ClassAdmin. If not, see <https://www.gnu.org/licenses/>.
# Copyright 2022 Ivan Heredia Planas
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

