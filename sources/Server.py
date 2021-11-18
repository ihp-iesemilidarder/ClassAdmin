import requests
from sources.utils import Environment, getIpAddress
class Server:
    @staticmethod
    def settingsChange(args):
        IP = requests.get("https://classadmin.server/api/server/address",headers={
            "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        }, verify=Environment.CA).json()["result"][0]["address"]
        print("your IP: "+getIpAddress())
        print(IP)
        if len(args)==2:
            Server.changePort(args[1])

        if getIpAddress()!=IP:
            requests.put("https://classadmin.server/api/server",headers={
                "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
            },
            data=f"address={getIpAddress()}",
            verify=Environment.CA)
            print("changing IP...")

    @staticmethod
    def changePort(port:int):
        PORT = requests.get("https://classadmin.server/api/server/port", headers={
            "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        }, verify=Environment.CA).json()["result"][0]["port"]

        if port!=PORT:
            requests.put("https://classadmin.server/api/server",headers={
                "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
            },
            data=f"port={port}",
            verify=Environment.CA)