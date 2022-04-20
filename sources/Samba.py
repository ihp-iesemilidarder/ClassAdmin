from sources.utils import logFile, Json, Environment
from sources.Requests import Requests
from smb.SMBConnection import SMBConnection
class Samba:

    @staticmethod
    def upload(filename,path):
        json = Json(Environment.data)
        server = Requests("services","GET","https://classadmin.server/api/servers/1").run().json()["result"]["ipaddress"]
        conn = SMBConnection(str(json.print(["Samba","username"])), str(json.print(["Samba","password"])), str(json.print(["Samba","shareDirectory"])), str(server), use_ntlm_v2 = True)
        conn.connect(server,139)
        with open(path,"rb") as file:
            conn.storeFile(json.print(["Samba","shareDirectory"]),filename,file)
        conn.close()