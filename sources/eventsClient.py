# Here, there are events required by the server
import platform,subprocess,time,os,datetime,pyscreenshot
from base64 import b64decode
from smb.SMBConnection import SMBConnection
from sources.utils import logFile, Notify, Environment, Json
from sources.Samba import Samba
class EventsClient:
    connection = None
    uri = ""
    def __init__(self):
        pass

    def run(self,message,conn):
        # Very IMPORTANT that you DOESN'T add a space after of the colons (:)
        # A example of message received:
        # text:this is comment.
        # function:functionName(arg1,arg2,...)
        connection = conn
        key,value = message.split(":",1)
        if key == "function":
            return exec(f"EventsClient.{value}")
        elif key == "text":
            logFile().message(Notify("comment",value,True),False,"INFO")
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
            if platform.system().upper() == "LINUX":
                path = f"/tmp/{filename}"
                screen = pyscreenshot.grab()
                screen.save(path)
            elif platform.system().upper() == "WINDOWS":
                subprocess.run(f"screenshot -o \"C:/Windows/Temp/{filename}\"")
            Samba.upload(filename,path)
            """with open(path,"rb") as file:
                conn = SMBConnection("ClassAdmin", "12345678", "ClassAdmin_Screenshots", "192.168.0.3", use_ntlm_v2 = True)
                conn.connect("192.168.0.3",139)
                conn.storeFile("ClassAdmin_Screenshots",filename,file)
                conn.close()"""
            os.remove(path)
            return True
        except:
            return False