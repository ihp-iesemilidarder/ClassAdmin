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
# This script file is used as module. Here is the functions and class used in all the project.
#
import os,socket,logging,json,psutil, platform, certifi,sys,subprocess

#This class storages all the paths for uses it in all the project
class Environment:
    hostsFile = "C:\\Windows\\System32\\drivers\\etc\\hosts" if platform.system().upper()=="WINDOWS" else "/etc/hosts" if platform.system().upper()=="LINUX" else None

    @staticmethod
    def SSL(type:str):
            return f"{os.environ['CLASSADMIN_SSL']}/ClassAdmin.{type}"

    commands = f"{os.environ['CLASSADMIN_HOME']}/commands"
    log = f"{os.environ['CLASSADMIN_LOG']}"
    transfers = f"{os.environ['CLASSADMIN_HOME']}/transfers"
    scripts = f"{os.environ['CLASSADMIN_HOME']}/sources/scripts"
    data = f"{os.environ['CLASSADMIN_HOME']}/sources/data.json"
    # <true> if <condition> else <true2> if <condition2> else None
    CA = f"{os.environ['CLASSADMIN_SSL']}/ClassAdmin.crt" if platform.system().upper()=="WINDOWS" else certifi.where() if platform.system().upper()=="LINUX" else None
    media = f"{os.environ['CLASSADMIN_HOME']}/sources/media"
    configuration = f"{os.environ['CLASSADMIN_HOME']}/services/ClassAdmin.conf"

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

    def print(self,path:list=False):
        if path:
            command = self.__command(path)
            return eval(command)
        else:
            return self.data

    def update(self,key:list,value):
        command = self.__command(key)
        try:
            try:
                # if the value is a list or integer....
                logFile().message(type(value))
                #add news types in the left
                if type(value) == list or int(value):
                    command+=f"={value}"
            except:
                # if the values is a string, will contains (')
                if type(value) == str:
                    command += f"='{value}'"
                else:
                    raise BaseException
        except:
            # else the value will be decode (everything bytes object is convert in string)
            command+=f"='{value.decode()}'"
        logFile(True).message(command)
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
    process = list(
        filter(
            lambda proc: True if str(proc.name()).upper().find(procName.upper()) != -1 or str("|".join(proc.cmdline())).upper().find(procName.upper()) != -1 else False,
            list(
                filter(
                    lambda proc: True if str(proc.name()).upper().find(procName.upper()) != -1 or str(proc.name()).upper().find("PYTHON") != -1 else False,
                    psutil.process_iter()
                )
            )
        )
    )
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
        return list(filter(lambda x: dns in x, IP))[0].split("\t")[0]

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
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8",80))
    ipaddress=sock.getsockname()[0]
    sock.close()
    return ipaddress

def Notify(title:str,message:str,output=True):
    status = Json(Environment.configuration).print(["notifications"])
    if(json.loads(status)):
        user = Json(Environment.configuration).print(["user"])
        architecture = platform.architecture()[0]
        zenity = f"zenity --notification --title \"{title}\" --text \"{message}\" --window-icon=\"{Environment.media}/images/ClassAdminLogo.png\" --display :0"
        toast = f"toast{architecture.replace('bit', '')} --title \"{title}\" --message \"{message}\" --icon \"{Environment.media}/images/ClassAdminLogo.png\" "
        command = f"su {user} -c '{zenity}'" if platform.system().upper() == 'LINUX' else toast
        os.system(command)
        if output:
            print(message)
            return message
