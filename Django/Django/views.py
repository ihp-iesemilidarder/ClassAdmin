import urllib3
from django.shortcuts import render
from .reqDashboard import ReqDashboard,RecoveryCodes
from django.http import JsonResponse
from sources.django import generateQR, styleStatusColor, loginAdmin
from sources.utils import Environment, Json
from sources.Requests import Requests
urllib3.disable_warnings()
jsonFile = Json(Environment.data).print()

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
        port = Requests("apache","GET","https://classadmin.server/api/servers").run().json()["result"][0]["port"]

        clients = Requests("apache","GET","https://classadmin.server/api/clients").run().json()["result"]
        jsonFile["pageDashboard"].update({
            "otpQR":generateQR,
            "port":port,
            "URIRecoveryCodes":RecoveryCodes().run(),
            "clients":clients,
            "styleStatusColor":styleStatusColor(),
            "checkNotification":str(Json(Environment.configuration).print(["notifications"])).lower(),
            "userNotification":Json(Environment.configuration).print(["user"])
        })
        return render(req,"pageDashboard.html",jsonFile["pageDashboard"])