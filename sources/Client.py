import urllib3
from sources.Requests import Requests
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

    # if the new client his ip address or nick is in the clients list
    def __differentHostAddress(self,ip,nick,clients):
        if clients==None:
            return True
        result = filter(lambda host: host["address"]==ip or host["nick"]==nick,clients)
        return True if len(list(result))==0 else False

    # this method adds or update clients
    # - This adds clients when these have ip address and nick new (not is in the list)
    # - This adds clients when the clients list is empty
    # - This update the clients when:
    #      - The client changes the ip address and use the same nick
    #      - The client changes the nick but the host has the same ip address
    # Deny connection when:
    # ---------------------
    #  - The client change the nick but this nick is active (exist in the clients list and his status is 'CONNECTED')

    def registre(self,nick,status):
        maxClientsConnected = Requests("services","GET",f"https://classadmin.server/api/servers").run().json()["result"][0]["clients"]
        clients = Requests("services","GET",f"https://classadmin.server/api/clients").run().json()["result"]
        client = Requests("services","GET",f"https://classadmin.server/api/clients/{self.address[0]}/{nick}").run().json()["result"]
        # if there are the clients maximum connected this throw a wrong
        if clients!=None and len(list(filter(lambda cli: cli["status"]=="CONNECTED",clients))) >= maxClientsConnected:
            return "TooManyClients"

        # if the clients list is empty and the host is different, this adds the new client in the list
        if (client==None and status=="CONNECTED") or (self.__differentHostAddress(self.address[0],nick,clients) and status=="CONNECTED"):
            Requests("services","POST",f"https://classadmin.server/api/clients",{
                    "nick":nick,
                    "address":self.address[0],
                    "port":self.address[1],
                    "status":status,
                    "server":1
            }).run()

        # if the new client's hostname is the same and is active (status CONNECTED), not add it
        elif self.__sameHostNameConnected(nick,self.address[0],"CONNECTED",clients):
            return "sameUser"

        # update the client
        else:
            cLientsUpdate = Requests("services","GET",f"https://classadmin.server/api/clients/{self.address[0]}/{nick}").run().json()["result"]
            # if there are more than one client, this deletes all minus one client for after update it
            if len(cLientsUpdate)>1:
                for cli in cLientsUpdate[0:len(cLientsUpdate)-1]:
                    Requests("services","DELETE",f"https://classadmin.server/api/clients/{cli['id']}").run().json()
            Requests("services","PUT",f"https://classadmin.server/api/clients/{self.address[0]}/{nick}",{
                    "nick":nick,
                    "address":self.address[0],
                    "port":self.address[1],
                    "status":status,
                    "server":1
            }).run()

        return True