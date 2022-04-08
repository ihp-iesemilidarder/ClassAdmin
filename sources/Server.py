import sys
from sources.utils import getIpAddress, logFile
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
            print(logFile().message(f"changing IP ipaddress to {getIpAddress()}...",True,"INFO"))

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
                print(logFile().message(err.args[1], err.args[2], "ERROR"))
            else:
                type, object, traceback = sys.exc_info()
                file = traceback.tb_frame.f_code.co_filename
                line = traceback.tb_lineno
                print(logFile().message(f"{err} in {file}:{line}", True, "ERROR"))