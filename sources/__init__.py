#This class storages all the paths for uses it in all the project
import os,socket,logging
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
    address=""
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8",80))
    address=sock.getsockname()[0]
    sock.close()
    return address

#This class write lines in the log file /var/log/ClassAdmin.log
class logFile:
    def __init__(self,django:bool=False):
        if django:
            Django = ': Django '
        else:
            Django = ''
        log_format = f"%(asctime)s - %(levelname)s {Django}: %(message)s"
        date_format = "%m/%d/%Y %I:%M:%S %p"
        logging.basicConfig(filename=Environment.pathLog(), level=logging.DEBUG, format=log_format,
                            datefmt=date_format)
        self.logger = logging.getLogger()
    def message(self,mess:str,output:bool=False,level:str=None) -> str:
        if level == "INFO":
            self.logger.info(mess)
        elif level == "DEBUG":
            self.logger.debug(mess)
        elif level == "WARNING":
            self.logger.warning(mess)
        else:
            self.logger.error(mess)
            level = "ERROR"
        if output:
            return mess
        else:
            return ""
