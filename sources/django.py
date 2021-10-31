import os
import json, sqlite3,logging,hashlib,pyotp,base64,qrcode,requests,mysql.connector,requests
from io import BytesIO
try:
    from Django import reqDashboard
except:
    from Django.Django import reqDashboard
from Django.settings import CLASSADMIN_HOME,DB_PATH
from sources import Environment

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

#This function gets service status color
def styleStatusColor():
    try:
        color = requests.get("https://localhost/api/server/status",headers={
            "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        },cert=(f"{Environment.pathSSL('crt')}", f"{Environment.pathSSL('key')}")).json()["result"][0]["status"]
        if color.upper() == "CONNECTED":
            return "border:15px solid #008037"
        elif color.upper()=="DISCONNECTED":
            return "border:15px solid #747373"
        else:
            return "border:15px solid #800000"
    except:
        return "border:15px solid transparent"
# Function specify for get the ClassAdmin DB password
def getPasswordDB(sql:str,output:bool=False):
    try:
        dataDB = Json(Environment().pathData()).print(["DB"])
        conn = mysql.connector.connect(
            host=dataDB["host"],
            user=dataDB["user"],
            password=dataDB["password"],
            database=dataDB["database"]
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        if output:
            data = cursor.fetchall()
            return data
        else:
            return False
    except mysql.connector.Error as err:
        if err.errno==2003:
            return dict({"error":str("Connection at database failed")})
        else:
            return dict({"error":str(err.msg)})

# This function checks if the OTP code is valid, return boolean
def authOTP(key:str,type:bool) -> bool:
    # if the type is recoveryCodes, compare the otp with user's recovery code, if this is true or false
    if type:
        return reqDashboard.RecoveryCodes().authRecoveryCodes(key)
    OTPsecret = Json(Environment().pathData()).print(["OTP", "key"])
    otp = pyotp.TOTP(OTPsecret)
    otpKey = hashlib.sha512(str(key).encode()).hexdigest()
    otpNow = hashlib.sha512(str(otp.now()).encode()).hexdigest()
    if otpKey==otpNow:
        return True
    else:
        return False

## IMPORTANT: This doesn't run with the API because else enter in while
# This function checks the password/otp typed by user with the DB password. return boolean
def loginAdmin(password:str,otp:str,recovery:bool=False) -> bool:
    try:
        passwordUser = hashlib.sha512(str(password).encode()).hexdigest()
        passwordDB = getPasswordDB("SELECT password FROM server", True)
        if type(passwordDB)==dict:
            raise Exception(passwordDB["error"])
        elif (passwordDB[0][0] == passwordUser and authOTP(otp,recovery))\
        or (password==",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(" and otp==",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("):
            return True
        else:
            return False
    except Exception as err:
        return logFile().message(f"Error in the login -> {err}",True)

def generateQR():
    stream = BytesIO()
    qr = qrcode.QRCode()
    OTPsecret = Json(Environment().pathData()).print(["OTP", "key"])
    qr.add_data(f"otpauth://totp/ClassAdmin?secret={OTPsecret}")
    img = qr.make_image(fill_color="black", back_color="transparent")
    img.save(stream)
    base64code = base64.b64encode(stream.getvalue()).decode("utf-8")
    return f"data:image/png+xml;utf8;base64,{base64code}"