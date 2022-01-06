import requests, time
from sources.utils import Environment

class Requests:
    sessionServices = requests.Session()
    sessionApache = requests.Session()
    headers = {
        "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
        "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
    }
    def __init__(self,session:str,method:str,url:str,data=None,headersExtra:dict={}):
        self.session=session
        Requests.headers.update(headersExtra)
        request = requests.Request(method,url,data=data,headers=Requests.headers)
        if session=="apache":
            self.prepared = Requests.sessionApache.prepare_request(request)
        elif session=="services":
            self.prepared = Requests.sessionServices.prepare_request(request)

    def run(self):
        time.sleep(1)
        if self.session=="apache":
            return Requests.sessionApache.send(self.prepared, verify=Environment.CA)
        elif self.session=="services":
            return Requests.sessionServices.send(self.prepared,verify=Environment.CA)