import json

from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from sources.django import loginAdmin
from ..models.Client import Client

class viewClient(View):

    def __dictfetchall(self,cursor):
        #Return all rows from a cursor as a dict
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    # Avoid the CSRF validate
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if str(request.headers).count("Password") == 0 or str(request.headers).count("Otp") == 0:
            return JsonResponse({"error":"You need authentication with password and otp"})
        elif not loginAdmin(request.headers['password'], request.headers["otp"]):
            return JsonResponse({"error":"Access denied"})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0,address=None,nick=None):
        if id != 0:
            client = list(Client.objects.filter(id=id).values())
            if len(client) > 0:
                client = client[0]
            else:
                client = None
        elif address != None and nick != None:
            client = list(Client.objects.filter(Q(address=address) | Q(nick=nick)).values())
            if len(client) == 0:
                client = None
        else:
            client = list(Client.objects.values())
            if len(client) == 0:
                client = None
        return JsonResponse({"result":client},safe=False)

    def post(self, request):
        data = json.loads(request.body)
        Client.objects.create(
            nick=data["nick"],
            address=data["address"],
            port=data["port"],
            status=data["status"],
            server=data["server"]
        )
        return JsonResponse({"result":True},safe=False)

    def put(self,request,id=0,address=None,nick=None):
        data = json.loads(request.body)
        if address != None and nick != None and id==0:
            client = list(Client.objects.filter(Q(address=address) | Q(nick=nick)).values())
        else:
            client = list(Client.objects.filter(id=id).values())
        if len(client) > 0:
            if address != None and nick != None and id == 0:
                client_object = Client.objects.get(Q(nick=nick) | Q(address=address))
            else:
                client_object = Client.objects.get(id=id)
            client_object.nick = data["nick"]
            client_object.address = data["address"]
            client_object.port = data["port"]
            client_object.status = data["status"]
            client_object.server = data["server"]
            client_object.save()
            result = {"result":True}
        else:
            result = {"result":False}
        return JsonResponse(result,safe=False)

    def patch(self,request,id):
        data = json.loads(request.body)

        # if searchs by status not id...
        if id == "CONNECTED" or id == "DISCONNECTED":
            client = list(Client.objects.filter(status=id).values())
            if len(client) > 0:
                cursor = connection.cursor()
                cursor.execute(f"UPDATE clients SET status='{data['status']}' WHERE status='{id}'")
                return JsonResponse({"result":True},safe=False)
            else:
                return JsonResponse({"result":False},safe=False)

        client = list(Client.objects.filter(id=id).values())
        if len(client) > 0:
            client_object = Client.objects.get(id=id)
            for key in data:
                exec(f"client_object.{key} = data[key]")
            client_object.save()
            result = {"result":True}
        else:
            result = {"result":None}
        return JsonResponse(result,safe=False)

    def delete(self,request,id):
        client = list(Client.objects.filter(id=id).values())
        if len(client) > 0:
            Client.objects.filter(id=id).delete()
            result = {"result":True}
        else:
            result = {"result":False}
        return JsonResponse(result,safe=False)