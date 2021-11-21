from sources.utils import Json, Environment
import requests

class ListClients:
    def __init__(self):
        self.clients = list(Json(Environment.data).print(["listClients"]))

    def add(self,element):
        numbersCLients = requests.get("https://classadmin.server/api/server/clients", headers={
            "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        }, verify=Environment.CA).json()["result"][0]["clients"]

        if len(self.clients) < numbersCLients:
            self.clients.append(f"{element}")
            Json(Environment.data).update(["listClients"],self.clients)
        else:
            element.send("Too many clients connected. You try it more later".encode("utf-8"))
            element.send(b"sig.SystemExit")
            raise SystemExit

    def remove(self,element):
        self.clients = list(filter(lambda socket: socket!=f"{element}",self.clients))
        Json(Environment.data).update(["listClients"], self.clients)

    def show(self):
        return self.clients