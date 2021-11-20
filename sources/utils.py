import os,socket,logging,json,psutil, time, platform, certifi, requests


#This class storages all the paths for uses it in all the project
class Environment:
    hostsFile = "C:\\Windows\\System32\\drivers\\etc" if platform.system().upper()=="WINDOWS" else "/etc/hosts" if platform.system().upper()=="LINUX" else None

    @staticmethod
    def SSL(type:str):
            return f"{os.environ['CLASSADMIN_SSL']}/ClassAdmin.{type}"

    @staticmethod
    def media(type):
        return f"{os.environ['CLASSADMIN_HOME']}/sources/media/{type}"

    log = f"{os.environ['CLASSADMIN_LOG']}"
    data = f"{os.environ['CLASSADMIN_HOME']}/sources/data.json"
    # <true> if <condition> else <true2> if <condition2> else None
    CA = f"{os.environ['CLASSADMIN_SSL']}/ClassAdmin.crt" if platform.system().upper()=="WINDOWS" else certifi.where() if platform.system().upper()=="LINUX" else None

#This class write lines in the log file /var/log/ClassAdmin.log
class logFile:
    def __init__(self,django:bool=False):
        if django:
            Django = ': Django '
        else:
            Django = ''
        log_format = f"%(asctime)s - %(levelname)s {Django}: %(message)s"
        date_format = "%m/%d/%Y %I:%M:%S %p"
        logging.basicConfig(filename=Environment.log, level=logging.DEBUG, format=log_format,
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

# This class operates with JSON files (show,save and write)
class Json:
    def __init__(self,file:str):
        self.file=file
        FileJson = open(self.file,"r")
        self.data = json.loads(FileJson.read())
        FileJson.close()

    def __command(self,path:list):
        command = "self.data"
        for element in path:
            command += f"['{element}']"
        return command

    def __save(self):
        with open(self.file,"w") as file:
            json.dump(self.data,file,indent=4)
            file.close()

    def print(self,path:list=False) -> str:
        if path:
            command = self.__command(path)
            return eval(command)
        else:
            return self.data

    def update(self,key:list,value):
        command = self.__command(key)
        try:
            if type(value) == list or int(value):
                command+=f"={value}"
        except:
            command+=f"='{value.decode()}'"
        exec(command)
        self.__save()

# system process' list
def systemProcess(key=None,value=None):
    if key and value:
        return list(
            filter(
                lambda proc:proc.info[key]==value,
                psutil.process_iter(["pid","status","username","name"])
            )
        )
    processList = []
    for process in psutil.process_iter(["pid","status","username","name"]):
        processList.append(process)
    return processList

def existProcess(procName:str):
    process = list(filter(lambda proc: proc.name()==procName,list(psutil.process_iter())))
    if len(process)>=1:
        return True
    else:
        return False

# class that works with system hosts file
class Hosts:
    @staticmethod
    def showIP(dns:str):
        file = open(Environment.hostsFile,"r")
        IP = file.read().split("\n")
        return list(filter(lambda x: "classadmin.server" in x, IP))[0].split("\t")[0]

    @staticmethod
    def new(hostname:str,ipNew:str,ipOld:str):

        # this does the changes
        file = open(Environment.hostsFile,"r")
        hostnames = file.read().split("\n")
        for line in hostnames:
            if hostname in line or ipOld in line:
                hostnames[hostnames.index(line)]=f"{ipNew}\t{hostname}"
            else:
                None
        file.close()

        # this writes the changes at hosts
        file = open(Environment.hostsFile,"w")
        file.write("\n".join(hostnames))
        file.close()

def getIpAddress():
    address=""
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8",80))
    address=sock.getsockname()[0]
    sock.close()
    return address