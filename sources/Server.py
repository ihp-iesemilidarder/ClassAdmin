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
# This Server class is used for change the server ip address or his port, so as close the the clients connecteds.
#
import sys
from sources.utils import getIpAddress, LogFile
from sources.Requests import Requests
class Server:

    # If at run the script, the server changes the port or ip ipaddress, update it at ClassAdmin DB
    @staticmethod
    def settingsChange(args):
        IP = Requests("services","GET","https://classadmin.server/api/servers").run().json()["result"][0]["ipaddress"]
        if len(args)==2:
            Server.changePort(args[1])

        if getIpAddress()!=IP:
            Requests("services","PATCH","https://classadmin.server/api/servers/1",{"ipaddress":getIpAddress()}).run()
            print(LogFile().message(f"changing IP ipaddress to {getIpAddress()}...", True, "INFO"))

    @staticmethod
    def changePort(port:int):
        PORT = Requests("services","GET","https://classadmin.server/api/servers").run().json()["result"][0]["port"]
        if port!=PORT:
            Requests("services","PATCH","https://classadmin.server/api/servers/1",{"port":port}).run()

    @staticmethod
    def closeClientsDB():
        try:
            Requests("apache","PATCH","https://classadmin.server/api/clients/CONNECTED",{"status":"DISCONNECTED"}).run()
        except BaseException as err:
            if err.args[0] == -5000:
                print(LogFile().message(err.args[1], err.args[2], "ERROR"))
            else:
                type, object, traceback = sys.exc_info()
                file = traceback.tb_frame.f_code.co_filename
                line = traceback.tb_lineno
                print(LogFile().message(f"{err} in {file}:{line}", True, "ERROR"))