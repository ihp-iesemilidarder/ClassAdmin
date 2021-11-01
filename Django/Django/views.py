import os
import sys,platform,urllib3,requests
from django.shortcuts import render, redirect
from Django.reqDashboard import ReqDashboard,RecoveryCodes
from django.http import HttpResponse,JsonResponse
from sources.django import generateQR, styleStatusColor, loginAdmin
from sources.utils import Environment, Json
if platform.system().upper() == "LINUX":
    sys.path.append("/etc/ClassAdmin")
elif platform.system().upper() == "WINDOWS":
    sys.path.append("C:\\Program Files\\ClassAdmin")
urllib3.disable_warnings()
jsonFile = Json(Environment().pathData()).print()

def pageLogin(req):
    # When the user does click, or event AJAX
    if req.is_ajax():
        try:
            login = loginAdmin(req.POST["password"],str(req.POST["otp"]))
        except Exception: # if the try does wrong, this means the otp is a recovery code
            login = loginAdmin(req.POST["password"], str(req.POST["recoveryCodes"]),True)
        return JsonResponse({"login":login,"styleStatusColor":""})
    else:
        return render(req,"pageLogin.html",jsonFile["pageLogin"])

def pageDashboard(req):
    if req.method == "POST":
        return JsonResponse({"result":ReqDashboard(req).run()})
    else:
        port = requests.get("https://localhost/api/server/port",headers={
            "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        },cert=(f"{Environment.pathSSL('crt')}", f"{Environment.pathSSL('key')}")).json()["result"][0]["port"]

        clients = requests.get("https://localhost/api/clients",headers={
            "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        },cert=(f"{Environment.pathSSL('crt')}", f"{Environment.pathSSL('key')}")).json()["result"]
        jsonFile["pageDashboard"].update({
            "otpQR":generateQR,
            "port":port,
            "URIRecoveryCodes":RecoveryCodes().run(),
            "nameFileRecoveryCodes":"recoveryCodes_ClassAdmin.txt",
            "clients":clients,
            "styleStatusColor":styleStatusColor()
        })
        return render(req,"pageDashboard.html",jsonFile["pageDashboard"])