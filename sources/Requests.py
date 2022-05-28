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
# This Requests class is used for to do reqeusts at ClassAdmin API Rest
#
import requests,json
from sources.utils import Environment
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
class Requests:
    sessionServices = requests.Session()
    sessionApache = requests.Session()
    # DON'T TOUCH, ELSE THIS THROW ERRORS IN REQUESTS: Maximum of error related in one request,
    # and for each retry delay 2 seconds
    retry = Retry(connect=10000,backoff_factor=2.0)
    adapter = HTTPAdapter(max_retries=retry)
    headers = {
        "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
        "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
    }
    sessionApache.mount("http://",adapter)
    sessionServices.mount("https://",adapter)
    def __init__(self,session:str,method:str,url:str,data=None,headersExtra:dict={}):
        self.session=session
        Requests.headers.update(headersExtra)
        request = requests.Request(method,url,data=json.dumps(data),headers=Requests.headers)
        if session=="apache":
            self.prepared = Requests.sessionApache.prepare_request(request)
        elif session=="services":
            self.prepared = Requests.sessionServices.prepare_request(request)

    def run(self):
        if self.session=="apache":
            return Requests.sessionApache.send(self.prepared, verify=Environment.CA)
        elif self.session=="services":
            return Requests.sessionServices.send(self.prepared,verify=Environment.CA)