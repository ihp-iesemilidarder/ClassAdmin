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
# This script file is responsible of do the requests at clients (shutdown,restart,etc.)
# Since JavaScript does a fetch() in the url '/dashboard'. Here gets the 'action' POST or 'notifications' POST and run his function.
# This functions use the pipeClient class for communicate his with the client program (EventsClient.py)
#
import base64,binascii,os,math,sys, json, random, platform,json
import time
from sources.django import generateQR
from sources.pipeClient import PipeClient
from sources.utils import Environment, LogFile, Json, existProcess
from sources.Requests import Requests
from sources.Server import Server
# This class contains the events functions of client
class ReqDashboard:
    def __init__(self,request):
        super()
        self.req = request

    def run(self):
        return EventsDashboard(self.req).run()

    def saveUserNotification(self,user:str):
        try:
            LogFile(True).message(f"user modified {user}", False)
            Json(Environment.configuration).update(["user"],user)
            return True
        except Exception as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            LogFile(True).message(f"Error during the OTP reload: {err} in {file}:{line}", False)
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
            LogFile(True).message(f"Error during the OTP reload: {err} in {file}:{line}", False)
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
            LogFile().message(f"{err} in {file}:{line}")
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
            LogFile().message(f"{err} in {file}:{line}")
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
            LogFile().message(f"{err} in {file}:{line}")
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
            LogFile().message(f"{err} in {file}:{line}")
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
            LogFile().message(f"{err} in {file}:{line}")
            return False

    def uploadFiles(self,id,name,file):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            n = 15000
            chunks = [str(file[i:i + n]) for i in range(0, len(file), n)]
            LogFile().message(chunks)
            for sector in chunks:
                PipeClient(str(currentHostName["ipaddress"])).send(f"function:downloadFile(None,'{name}','{sector}',{'True' if chunks.index(sector)==len(chunks)-1 else 'False'})")
                time.sleep(.5)
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            LogFile().message(f"{err} in {file}:{line}")
            return False

    def deleteFile(self,id,filename):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName["ipaddress"])).send(f"function:deleteFile(None,'{filename}')")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            LogFile().message(f"{err} in {file}:{line}")
            return False

    def screenshot(self,id):
        try:
            server = Requests("apache", "GET", f"https://classadmin.server/api/servers/1").run().json()["result"]
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName["ipaddress"])).send(f"function:screenshot('{currentHostName['hostname']}')")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_csode.co_filename
            line = traceback.tb_lineno
            LogFile().message(f"{err} in {file}:{line}")
            return False

    def listPrograms(self,id):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName["ipaddress"])).send(f"function:listPrograms()")
            time.sleep(5)
            with open(f"{Environment.transfers}/.screenshots/listPrograms.txt","rb") as file:
                data = json.loads(file.read())
            os.remove(f"{Environment.transfers}/.screenshots/listPrograms.txt")
            return data
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            LogFile().message(f"{err} in {file}:{line}")
            return False

    def denyPrograms(self,id,list):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            PipeClient(str(currentHostName["ipaddress"])).send(f"function:denyPrograms('{list}')")
            return True
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            LogFile().message(f"{err} in {file}:{line}")
            return False

    def deleteClient(self,id):
        try:
            currentHostName = Requests("apache", "GET", f"https://classadmin.server/api/clients/{id}").run().json()["result"]
            Requests("apache", "DELETE", f"https://classadmin.server/api/clients/{id}").run()
            PipeClient(str(currentHostName["ipaddress"])).send(f"function:closeClient()")
            return True
        except BaseException as err:
            Requests("apache", "DELETE", f"https://classadmin.server/api/clients/{id}").run()
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            LogFile().message(f"{err} in {file}:{line}")
            return False

# This class call to the events functions of client (shutdown,edit hostname,alert,etc)
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
        elif self.req.POST["action"] == "deleteFile":
            id,filename = self.req.POST["id"],self.req.POST["filename"]
            return super().deleteFile(id,filename)
        elif self.req.POST["action"] == "screenshot":
            id = self.req.POST["id"]
            return super().screenshot(id)
        elif self.req.POST["action"] == "listPrograms":
            id = self.req.POST["id"]
            return super().listPrograms(id)
        elif self.req.POST["action"] == "denyPrograms":
            id, list = self.req.POST["id"], self.req.POST["list"]
            return super().denyPrograms(id,list)
        elif self.req.POST["action"] == "deleteClient":
            id = self.req.POST["id"]
            return super().deleteClient(id)

    def __notifications(self):
        try:
            Json(Environment.configuration).update(["notifications"], self.req.POST["notifications"])
            return True
        except Exception as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            LogFile(True).message(f"Error at disable/enable the notifications: {err} in {file}:{line}", False)
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
            LogFile(True).message(f"Error at generate URI recoveryCodes OTP: {err} in {file}:{line}", False)
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
            LogFile(True).message(f"Error during the download recoveryCodes OTP: {err} in {file}:{line}", False)
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