from sources.utils import getIpAddress, logFile
from sources.Requests import Requests
class Server:

    # If at run the script, the server changes the port or ip address, update it at ClassAdmin DB
    @staticmethod
    def settingsChange(args):
        IP = Requests("services","GET","https://classadmin.server/api/server/address").run().json()["result"][0]["address"]
        if len(args)==2:
            Server.changePort(args[1])

        if getIpAddress()!=IP:
            Requests("services","PUT","https://classadmin.server/api/server",f"address={getIpAddress()}").run()
            print(logFile().message(f"changing IP address to {getIpAddress()}...",True,"INFO"))

    @staticmethod
    def changePort(port:int):
        PORT = Requests("services","GET","https://classadmin.server/api/server/port").run().json()["result"][0]["port"]
        if port!=PORT:
            Requests("services","PUT","https://classadmin.server/api/server",f"port={port}").run()