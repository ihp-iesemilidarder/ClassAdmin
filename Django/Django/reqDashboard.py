import base64,binascii,os,math,sys, json, random, platform
import time

from sources.django import generateQR
from sources.pipeClient import PipeClient
from sources.utils import Environment, logFile, Json, existProcess
from sources.Requests import Requests
from sources.Server import Server

class ReqDashboard:
    def __init__(self,request):
        super()
        self.req = request

    def run(self):
        return EventsDashboard(self.req).run()

    def saveUserNotification(self,user:str):
        try:
            logFile(True).message(f"user modified {user}", False)
            Json(Environment.configuration).update(["user"],user)
            return True
        except Exception as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile(True).message(f"Error during the OTP reload: {err} in {file}:{line}", False)
            return False

    def showData(self):
        port = Requests("apache","GET","https://classadmin.server/api/servers").run().json()["result"][0]["port"]
        userNotification = Json(Environment.configuration).print(["user"])
        isNotification = Json(Environment.configuration).print(["notifications"])
        return {
            "port":port,
            "userNotification":userNotification,
            "isNotification":json.loads(isNotification.lower())
        }

    #Reloads the OTP QR code
    def reloadOTP(self):
        try:
            code = binascii.b2a_hex(os.urandom(15))
            key = base64.b32encode(base64.b16decode(code.upper()))
            Json(Environment.data).update(["OTP", "key"], key)
            return generateQR()
        except Exception as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile(True).message(f"Error during the OTP reload: {err} in {file}:{line}", False)
            return False

    def shutdownHost(self,id):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName["ipaddress"])).send("function:shutdownHost()")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(f"{err} in {file}:{line}")
            return False

    def rebootHost(self,id):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName["ipaddress"])).send("function:rebootHost()")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(f"{err} in {file}:{line}")
            return False

    def suspendHost(self,id):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName["ipaddress"])).send("function:suspendHost()")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(f"{err} in {file}:{line}")
            return False

    def editHostName(self,id,hostname):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName['ipaddress'])).send(f"function:editHostName('{hostname}')")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(f"{err} in {file}:{line}")
            return False

    def sendAlert(self,id,tipe,title,description):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName["ipaddress"])).send(f"function:sendAlert('{tipe}','{title}','{description}')")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(f"{err} in {file}:{line}")
            return False

    def uploadFiles(self,id,name,file):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            n = 15000
            chunks = [str(file[i:i + n]) for i in range(0, len(file), n)]
            logFile().message(chunks)
            for sector in chunks:
                PipeClient(str(currentHostName["ipaddress"])).send(f"function:downloadFile('{currentHostName['hostname']}','{name}','{sector}',{'True' if chunks.index(sector)==len(chunks)-1 else 'False'})")
                time.sleep(.5)
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile().message(f"{err} in {file}:{line}")
            return False

# events for each client (shutdown,edit hostnamename,alert,etc)
class EventsDashboard(ReqDashboard):
    def __init__(self,req):
        super().__init__(req)

    def run(self):
        if "action" in self.req.POST:
            return self.__actions()
        elif "notifications" in self.req.POST:
            return self.__notifications()


    def __actions(self):
        if self.req.POST["action"] == "newOTP":
            return super().reloadOTP()
        elif self.req.POST["action"] == "keepAlive":
            if platform.system().upper() == "WINDOWS" and existProcess("ClassAdminS") == False:
                Server.closeClientsDB()
            return existProcess("ClassAdminS")
        elif self.req.POST["action"] == "showData":
            return super().showData()
        elif self.req.POST["action"] == "saveUserNotification":
            return super().saveUserNotification(self.req.POST["user"])
        elif self.req.POST["action"] == "editHostName":
            id, hostname = self.req.POST["id"],self.req.POST["hostname"]
            return super().editHostName(id,hostname)
        elif self.req.POST["action"] == "shutdownHost":
            id = self.req.POST["id"]
            return super().shutdownHost(id)
        elif self.req.POST["action"] == "rebootHost":
            id = self.req.POST["id"]
            return super().rebootHost(id)
        elif self.req.POST["action"] == "suspendHost":
            id = self.req.POST["id"]
            return super().suspendHost(id)
        elif self.req.POST["action"] == "sendAlert":
            id,tipe,title,description = self.req.POST["id"],self.req.POST["type"],self.req.POST["title"],self.req.POST["description"]
            return super().sendAlert(id,tipe,title,description)
        elif self.req.POST["action"] == "uploadFiles":
            id,name,file = self.req.POST["id"],self.req.POST["name"],self.req.POST["file"]
            return super().uploadFiles(id,name,file)

    def __notifications(self):
        try:
            Json(Environment.configuration).update(["notifications"], self.req.POST["notifications"])
            return True
        except Exception as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile(True).message(f"Error at disable/enable the notifications: {err} in {file}:{line}", False)
            return f"Error at disable/enable the notifications: {err} in {file}:{line}"

# This class generates the OTP recovery Codes
class RecoveryCodes:
    def __init__(self):
        return None

    def run(self):
        arrayRecoveryCodes = self.__checkCodes()
        return self.__generateFileRecoveryCodes(arrayRecoveryCodes)

    def __generateCode(self,len: int, separator: str) -> str:
        left = math.floor(len / 2)
        right = len - left
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        code = random.sample(numbers, left)
        code.append(separator)
        code += random.sample(numbers, right)
        return "".join(code)

    def __printCode(self,list,index):
        try:
            return list[index]
        except Exception:
            return ""

    def __generateFileRecoveryCodes(self,codes):
        try:
            text,first="",0
            for y in range(0,math.ceil(len(codes)/5)):
                text+=f"{self.__printCode(codes,first)}    {self.__printCode(codes,first + 1)}    {self.__printCode(codes,first + 2)}    {self.__printCode(codes,first + 3)}    {self.__printCode(codes,first + 4)}\n"
                first+=5
            b64 = base64.b64encode(text.encode()).decode('utf-8')
            return f"data:text/plain;utf8;base64,{b64}"
        except Exception as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile(True).message(f"Error at generate URI recoveryCodes OTP: {err} in {file}:{line}", False)
            return False

    def __checkCodes(self):
        try:
            arrayCodes = Json(Environment.data).print(["OTP", "recoveryCodes"])
            if len(arrayCodes)==0:
                codes = []
                for code in range(0, 20):
                    codes.append(self.__generateCode(6, "-"))
                Json(Environment.data).update(["OTP", "recoveryCodes"], codes)
            arrayCodesUpdated = Json(Environment.data).print(["OTP", "recoveryCodes"])
            return arrayCodesUpdated
        except Exception as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            logFile(True).message(f"Error during the download recoveryCodes OTP: {err} in {file}:{line}", False)
            return False

    def authRecoveryCodes(self,key:str) -> bool:
        codes = Json(Environment.data).print(["OTP", "recoveryCodes"])
        if key in codes:
            self.__removeRecoveryCode(key,codes)
            return True
        return False

    def __removeRecoveryCode(self,key:str,array:list):
        array.remove(key)
        Json(Environment.data).update(["OTP", "recoveryCodes"], array)