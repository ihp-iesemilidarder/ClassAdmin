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
import urllib3
from django.shortcuts import render
from .reqDashboard import ReqDashboard,RecoveryCodes
from django.http import JsonResponse
from sources.django import generateQR, styleStatusColor, loginAdmin
from sources.utils import Environment, Json
from sources.Requests import Requests
urllib3.disable_warnings()
jsonFile = Json(Environment.data).print()

# fumction of main page
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

# function of 'dashboard/' url
def pageDashboard(req):
    # if the user do a request to /dashboard will run this if statement
    if req.method == "POST":
        return JsonResponse({"result":ReqDashboard(req).run()})
    else:
        # This run the dashboard webpage
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