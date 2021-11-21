import requests, urllib3
from sources.utils import Environment
from sources.notification import Notify
urllib3.disable_warnings()
class Client:
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address

    def registre(self,nick,status,conscent):
        client = requests.get(f"https://classadmin.server/api/clients?address={self.address[0]}&|nick={nick}",headers={
                "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        },verify=Environment.CA).json()
        """if client!=None and status=="CONNECTED" and conscent==True:
            connection.send("Conscent: Do you want to change the nick or nick's ip address?".encode("utf-8"))
            if conscent == None:
                raise SystemExit"""
        if client["result"]==None:
            requests.post(f"https://classadmin.server/api/clients",
                headers={
                    "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
                },
                data=f"nick={nick}&address={self.address[0]}&port={self.address[1]}&status={status}&cli_ser_id=1",
                verify=Environment.CA
            )
        elif client["result"][0]["address"]!=self.address[0] and client["result"][0]["nick"]==nick and client["result"][0]["status"]=="CONNECTED":
            return False
        else:
            requests.put(f"https://classadmin.server/api/clients?address={self.address[0]}",
                headers={
                    "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
                },
                data=f"nick={nick}&address={self.address[0]}&port={self.address[1]}&status={status}&cli_ser_id=1",
                verify=Environment.CA
            )
        return True