import base64,binascii,os,math
import random
from sources.django import generateQR
from sources.utils import Environment, logFile, Json

class ReqDashboard:
    def __init__(self,request):
        self.req = request

    def run(self):
        if self.req.POST["action"] == "newOTP":
            return self.__reloadOTP()

    #Reloads the OTP QR code
    def __reloadOTP(self):
        try:
            code = binascii.b2a_hex(os.urandom(15))
            key = base64.b32encode(base64.b16decode(code.upper()))
            Json(Environment.data).update(["OTP", "key"], key)
            return generateQR()
        except Exception as err:
            logFile(True).message(f"Error during the OTP reload: {err}", False)
            return False

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
            logFile(True).message(f"Error at generate URI recoveryCodes OTP: {err}", False)
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
            logFile(True).message(f"Error during the download recoveryCodes OTP: {err}", False)
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