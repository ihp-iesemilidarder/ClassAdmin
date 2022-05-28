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
# This script file is used as module. This is used in the app Django.
#
import hashlib,pyotp,base64,qrcode,mysql.connector
from io import BytesIO
# this import is inside a try because the sockets files need it, and since his path is different the import path also is different
try:
    from Django import reqDashboard
except:
    from Django.Django import reqDashboard
from sources.utils import Environment, Json,logFile, existProcess

#This function gets service status color
def styleStatusColor():
    try:
        if existProcess("ClassAdminS"):
            return "border:15px solid #008037"
        else:
            return "border:15px solid #747373"
    except:
        return "border:15px solid transparent"

# Function specify for get the ClassAdmin DB password
def getPasswordDB(sql:str,output:bool=False):
    try:
        dataDB = Json(Environment.data).print(["DB"])
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
    OTPsecret = Json(Environment.data).print(["OTP", "key"])
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

        # I use password/otp static for can program the requests API
        elif (passwordDB[0][0] == passwordUser and authOTP(otp,recovery))\
        or (passwordDB[0][0] == passwordUser and otp==",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(")\
        or (password==",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(" and otp==",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("):
            return True
        else:
            return False
    except Exception as err:
        return logFile().message(f"Error in the login -> {err}",True)

def generateQR():
    stream = BytesIO()
    qr = qrcode.QRCode()
    OTPsecret = Json(Environment.data).print(["OTP", "key"])
    qr.add_data(f"otpauth://totp/ClassAdmin?secret={OTPsecret}")
    img = qr.make_image(fill_color="black", back_color="transparent")
    img.save(stream)
    base64code = base64.b64encode(stream.getvalue()).decode("utf-8")
    return f"data:image/png+xml;utf8;base64,{base64code}"