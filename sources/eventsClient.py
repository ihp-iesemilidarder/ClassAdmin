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
# This EventsClient class is used in Client program (ClassAdmin.socket).
# Here is the functions called since Django app of each client.
#
import platform,subprocess,time,os,datetime,pyscreenshot,sys
from base64 import b64decode
from sources.utils import logFile, Notify, Environment, Json
from sources.Samba import Samba
from sources.Requests import Requests
from sources.pipeClient import PipeClient
class EventsClient:
    connection = None
    uri = ""
    def __init__(self):
        pass

    def run(self,message):
        # Very IMPORTANT that you DOESN'T add a space after of the colons (:)
        # A example of message received:
        # text:this is comment.
        # function:functionName(arg1,arg2,...)
        key,value = message.split(":",1)
        logFile().message(key)
        if key == "function":
            return exec(f"EventsClient.{value}")
        elif key == "text":
            logFile().message(Notify("comment",value,True),True,"INFO")
            return True

    @staticmethod
    def shutdownHost():
        logFile().message(Notify("shutdown","This computer will power off",True),False,"INFO")
        if platform.system().upper() == "WINDOWS":
            subprocess.run("shutdown -s")
            return True
        elif platform.system().upper() == "LINUX":
            time.sleep(5)
            subprocess.run("poweroff")
            return True

    @staticmethod
    def rebootHost():
        logFile().message(Notify("restart","This computer will restarted",True),False,"INFO")
        if platform.system().upper() == "WINDOWS":
            subprocess.run("shutdown -r")
            return True
        elif platform.system().upper() == "LINUX":
            time.sleep(5)
            subprocess.run("reboot")
            return True

    @staticmethod
    def suspendHost():
        logFile().message(Notify("suspend","This computer will suspended",True),False,"INFO")
        if platform.system().upper() == "WINDOWS":
            subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return True
        elif platform.system().upper() == "LINUX":
            time.sleep(5)
            subprocess.run("pm-suspend")
            return True

    @staticmethod
    def editHostName(newHostname:str) -> bool:
        Notify("Rename hostname",f"The computer will be change his hostname to {newHostname}.")
        time.sleep(3)
        if platform.system().upper() == "LINUX":
            subprocess.run([f"{Environment.scripts}/Linux/editHostName.sh",newHostname,"&"])
            return True
        elif platform.system().upper() == "WINDOWS":
            Notify("Reboot","You computer will be reboot in 10 seconds")
            time.sleep(10)
            subprocess.run(["powershell.exe",f"& '{Environment.scripts}/Windows/editHostName.ps1' -newHostName {newHostname}"])
            return True

    @staticmethod
    def sendAlert(tipe:str,title:str,description:str) -> bool:
        if tipe=="notification":
            Notify(title,description,False)
        else:
            zenity = f"zenity --{tipe} --title '{title}' --text '{description}' --window-icon='{Environment.media}/images/ClassAdminLogo.png'"
            user = Json(Environment.configuration).print(["user"])
            if platform.system().upper()=="LINUX":
                os.system(f"su {user} -c \"{zenity}\"")
            elif platform.system().upper()=="WINDOWS":
                architecture = platform.architecture()[0]
                os.system(f"toast{architecture.replace('bit', '')} --title \"{title}\" --message \"{description}\" --icon \"{Environment.media}/images/{tipe}.png\"")
        return True

    @staticmethod
    def saveFile(hostname,name:str):
        if hostname!=None:
            path = f"{Environment.transfers}/{hostname}"
        else:
            path = f"{Environment.transfers}/server"
        file = open(f"{path}/{name}.datauri","r")
        uri = file.read().replace(" ","+")
        file.close()
        headers,encoded = uri.split(",",1)
        data = b64decode(encoded)
        with open(f"{path}/{name}", "wb") as f:
            f.write(data)
        os.remove(f"{path}/{name}.datauri")
        Notify(f"file transfers by {'the server' if hostname==None else hostname}",f"the {'server' if hostname==None else f'client {hostname}'} shared you a file: {name}",False)
        return True

    @staticmethod
    def downloadFile(hostname,name:str,sector:str,last:bool) -> bool:
        if hostname!=None:
            path = f"{Environment.transfers}/{hostname}"
            try:
                os.makedirs(path)
            except:
                None
        else:
            path = f"{Environment.transfers}/server"
        with open(f"{path}/{name}.datauri", "a+") as f:
            f.write(sector)
        if last:
            EventsClient.saveFile(hostname,name)

    @staticmethod
    def deleteFile(hostname,filename:str):
        try:
            if hostname==None:
                path = f"{Environment.transfers}/server"
            else:
                path = f"{Environment.transfers}/{hostname}"
            os.remove(f"{path}/{filename}")
            return True
        except:
            return False

    @staticmethod
    def screenshot(id):
        try:
            date = datetime.datetime.now()
            filename = f"ClassAdmin_screenshot_{date.day}-{date.month}-{date.year}_{date.hour}-{date.minute}-{date.second}.png"
            path = f"/tmp/{filename}" if platform.system().upper() == "LINUX" else f"C:/Windows/Temp/{filename}" if platform.system().upper()=="WINDOWS" else None
            screen = pyscreenshot.grab()
            screen.save(path)
            if platform.system().upper() == "LINUX":
                Samba.upload(filename,path)
            elif platform.system().upper() == "WINDOWS":
                server = Json(Environment.data).print(["Samba", "server"])
                username = Json(Environment.data).print(["Samba","username"])
                password = Json(Environment.data).print(["Samba","password"])
                sharedDirectory = Json(Environment.data).print(["Samba","sharedDirectory"])
                subprocess.run(["powershell.exe",f"& '{Environment.scripts}/Windows/sharedDirectory.ps1' -Operation Add -Server {server} -Username {username} -Password {password} -SharedDirectory {sharedDirectory} -FileName {filename} -File {path}"])
            logFile().message(Notify("Screenshot","The ClassAdmin admin did one screenshot of your desktop",True),False,"INFO")
            os.remove(path)
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
            Notify("Error unexpected at save the screenshot","You check if you has access a shared folder ClassAdmin_Screenshots",False)
            return False

    @staticmethod
    def listPrograms():
        try:
            server = Json(Environment.data).print(["Samba", "server"])
            username = Json(Environment.data).print(["Samba", "username"])
            password = Json(Environment.data).print(["Samba", "password"])
            sharedDirectory = Json(Environment.data).print(["Samba", "sharedDirectory"])
            if platform.system().upper()=="WINDOWS":
                subprocess.run(["powershell.exe",f"& '{Environment.scripts}/Windows/listPrograms.ps1' -SharedDestination \\\\{server}\\{sharedDirectory} -Username {username} -Password {password}"])
            elif platform.system().upper()=="LINUX":
                subprocess.run([f"{Environment.scripts}/Linux/listPrograms.sh",server,sharedDirectory,username,password,"&"])
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
            Notify("Error unexpected at save the screenshot","You check if you has access a shared folder ClassAdmin_Screenshots",False)
            return False

    @staticmethod
    def denyPrograms(programs:str):
        try:
            if platform.system().upper()=="WINDOWS":
                subprocess.run(["powershell.exe",f"& '{Environment.scripts}/Windows/denyPrograms.ps1' -Programs '{programs}'"])
            elif platform.system().upper()=="LINUX":
                subprocess.run([f"{Environment.scripts}/Linux/denyPrograms.sh",f'{programs.replace(","," ")}',"&"])
            if programs=="null":
                Notify("DenyClass","The administrator allowed all the programs")
            else:
                Notify("DenyClass","The administrator denied same programs")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
            Notify("DenyClass","Error unexpected at deny the programs",False)
            return False
    @staticmethod
    def closeClient():
        try:
            if platform.system().upper()=="WINDOWS":
                subprocess.run(["nssm","ClassAdmin","stop"])
            elif platform.system().upper()=="LINUX":
                subprocess.run(["systemctl","stop","ClassAdmin"])
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
            Notify("Error unexpected at close the client",False)
            return False