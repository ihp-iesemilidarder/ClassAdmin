# Here, there are events required by the server
import platform,subprocess,time,os

from sources.utils import logFile, Notify, Environment, Json
class EventsClient:
    def __init__(self):
        pass

    def run(self,message):
        # Very IMPORTANT that you DOESN'T add a space after of the colons (:)
        # A example of message received:
        # text:this is comment.
        # function:functionName(arg1,arg2,...)
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
    def editNickName(currentNick:str,newNick:str) -> bool:
        if platform.system().upper() == "LINUX":
            subprocess.run([f"{Environment.scripts}/Linux/editNickName.sh",currentNick,newNick,"&"])
            return True
        elif platform.system().upper() == "WINDOWS":
            subprocess.run(["powershell.exe",f"& '{Environment.scripts}/Windows/editNickName.ps1' -newNickName {newNick}"])
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
    def downloadFile(nick:str,name:str,data:str) -> bool:
        path = f"{Environment.transfers}/{nick}"
        try:
            os.makedirs(path)
        except:
            None
        with open(f"{path}/{name}","w") as file:
            file.write(data)
        return True