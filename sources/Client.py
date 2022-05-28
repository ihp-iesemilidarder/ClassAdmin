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
# This Client class registres each client connected, adding it at ClassAdmin database. So checks before of register it, if the client is not duplicated, connected, etc.
#
import urllib3
from sources.Requests import Requests
urllib3.disable_warnings()
class Client:
    def __init__(self,connection,ipaddress):
        self.connection = connection
        self.ipaddress = ipaddress

    # if the hostname of new client is in the list
    def __sameHostNameConnected(self,hostname,ipaddress,status,clients):
        result = filter(
            lambda host: host["hostname"]==hostname and host["ipaddress"]!=ipaddress and host["status"]==status,
            clients
        )
        return True if len(list(result))>0 else False

    # if the new client his ip ipaddress or hostname is in the clients list
    def __differentHostAddress(self,ip,hostname,clients):
        if clients==None:
            return True
        result = filter(lambda host: host["ipaddress"]==ip or host["hostname"]==hostname,clients)
        return True if len(list(result))==0 else False

    # this method adds or update clients
    # - This adds clients when these have ip ipaddress and hostname new (not is in the list)
    # - This adds clients when the clients list is empty
    # - This update the clients when:
    #      - The client changes the ip ipaddress and use the same hostname
    #      - The client changes the hostname but the host has the same ip ipaddress
    # Deny connection when:
    # ---------------------
    #  - The client change the hostname but this hostname is active (exist in the clients list and his status is 'CONNECTED')

    def registre(self,hostname,status):
        maxClientsConnected = Requests("services","GET",f"https://classadmin.server/api/servers").run().json()["result"][0]["clients"]
        clients = Requests("services","GET",f"https://classadmin.server/api/clients").run().json()["result"]
        client = Requests("services","GET",f"https://classadmin.server/api/clients/{self.ipaddress[0]}/{hostname}").run().json()["result"]
        # if there are the clients maximum connected this throw a wrong
        if clients!=None and len(list(filter(lambda cli: cli["status"]=="CONNECTED",clients))) >= maxClientsConnected:
            return "TooManyClients"

        # if the clients list is empty and the host is different, this adds the new client in the list
        if (client==None and status=="CONNECTED") or (self.__differentHostAddress(self.ipaddress[0],hostname,clients) and status=="CONNECTED"):
            Requests("services","POST",f"https://classadmin.server/api/clients",{
                    "hostname":hostname,
                    "ipaddress":self.ipaddress[0],
                    "port":self.ipaddress[1],
                    "status":status,
                    "server":1
            }).run()

        # if the new client's hostname is the same and is active (status CONNECTED), not add it
        elif self.__sameHostNameConnected(hostname,self.ipaddress[0],"CONNECTED",clients):
            return "sameUser"

        # update the client
        else:
            cLientsUpdate = Requests("services","GET",f"https://classadmin.server/api/clients/{self.ipaddress[0]}/{hostname}").run().json()["result"]
            # if there are more than one client, this deletes all minus one client for after update it
            if len(cLientsUpdate)>1:
                for cli in cLientsUpdate[0:len(cLientsUpdate)-1]:
                    Requests("services","DELETE",f"https://classadmin.server/api/clients/{cli['id']}").run().json()
            Requests("services","PUT",f"https://classadmin.server/api/clients/{self.ipaddress[0]}/{hostname}",{
                    "hostname":hostname,
                    "ipaddress":self.ipaddress[0],
                    "port":self.ipaddress[1],
                    "status":status,
                    "server":1
            }).run()

        return True