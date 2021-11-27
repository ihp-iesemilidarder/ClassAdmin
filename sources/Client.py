import requests, urllib3
from sources.utils import Environment
from sources.notification import Notify
urllib3.disable_warnings()
class Client:
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address

    # if the hostname of new client is in the list
    def __sameHostNameConnected(self,nick,address,status,clients):
        result = filter(
            lambda host: host["nick"]==nick and host["address"]!=address and host["status"]==status,
            clients
        )
        return True if len(list(result))>0 else False

    # if the new client his ip address is in the clients list
    def __differentHostAddress(self,ip,nick,clients):
        if clients==None:
            return True
        result = filter(lambda host: host["address"]==ip or host["nick"]==nick,clients)
        return True if len(list(result))==0 else False

    def registre(self,nick,status,conscent):
        clients = requests.get(f"https://classadmin.server/api/clients",headers={
                "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        },verify=Environment.CA).json()["result"]

        client = requests.get(f"https://classadmin.server/api/clients?address={self.address[0]}&|nick={nick}",headers={
                "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        },verify=Environment.CA).json()["result"]
        """if client!=None and status=="CONNECTED" and conscent==True:
            connection.send("Conscent: Do you want to change the nick or nick's ip address?".encode("utf-8"))
            if conscent == None:
                raise SystemExit"""

        # if the clients list is empty and the host is different, this adds the new client in the list
        if (client==None and status=="CONNECTED") or self.__differentHostAddress(self.address[0],nick,clients):
            requests.post(f"https://classadmin.server/api/clients",
                headers={
                    "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
                },
                data=f"nick={nick}&address={self.address[0]}&port={self.address[1]}&status={status}&cli_ser_id=1",
                verify=Environment.CA
            )

        # if the new client's hostname is the same, not add it
        elif self.__sameHostNameConnected(nick,self.address[0],"CONNECTED",clients):
            return False
        # update client
        else:
            requests.put(f"https://classadmin.server/api/clients?address={self.address[0]}&|nick={nick}",
                headers={
                    "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
                },
                data=f"nick={nick}&address={self.address[0]}&port={self.address[1]}&status={status}&cli_ser_id=1",
                verify=Environment.CA
            )
        return True