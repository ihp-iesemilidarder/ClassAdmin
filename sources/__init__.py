#This class storages all the paths for uses it in all the project
import os,socket
class Environment:
    def __init__(self):
        self.directory = os.environ["CLASSADMIN_HOME"]

    @staticmethod
    def pathDB(self) -> str:
        return DB_PATH

    @staticmethod
    def pathLog() -> str:
        return f"{os.environ['CLASSADMIN_LOG']}"

    def pathData(self) -> str:
        return f"{self.directory}/sources/data.json"

    @staticmethod
    def pathSSL(type:str):
            return f"{os.environ['CLASSADMIN_SSL']}/ClassAdmin.{type}"

def getIpAddress():
    address="";
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8",80))
    address=sock.getsockname()[0]
    sock.close()
    return address