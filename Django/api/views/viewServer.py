import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from sources.django import loginAdmin
from ..models.Server import Server

class viewServer(View):

    # Avoid the CSRF validate
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if str(request.headers).count("Password") == 0 or str(request.headers).count("Otp") == 0:
            return JsonResponse({"error":"You need authentication with password and otp"})
        elif not loginAdmin(request.headers['password'], request.headers["otp"]):
            return JsonResponse({"error":"Access denied"})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        print(Server.objects)
        if id != 0:
            server = list(Server.objects.filter(id=id).values())
            if len(server) > 0:
                server = server[0]
            else:
                server = None
        else:
            server = list(Server.objects.values())
            if not len(server) > 0:
                server = None
        return JsonResponse({"result":server},safe=False)

    def post(self, request):
        data = json.loads(request.body)
        Server.objects.create(
            password=data["password"],
            ipaddress=data["ipaddress"],
            port=data["port"],
            clients=data["clients"]
        )
        return JsonResponse({"result":True},safe=False)

    def put(self,request,id):
        data = json.loads(request.body)
        server = list(Server.objects.filter(id=id).values())
        if len(server) > 0:
            server_object = Server.objects.get(id=id)
            server_object.password = data["password"]
            server_object.ipaddress = data["ipaddress"]
            server_object.port = data["port"]
            server_object.clients = data["clients"]
            server_object.save()
            result = {"result":True}
        else:
            result = {"result":False}
        return JsonResponse(result,safe=False)

    def patch(self,request,id):
        data = json.loads(request.body)
        server = list(Server.objects.filter(id=id).values())
        if len(server) > 0:
            server_object = Server.objects.get(id=id)
            for key in data:
                exec(f"server_object.{key} = data[key]")
            server_object.save()
            result = {"result":True}
        else:
            result = {"result":False}
        return JsonResponse(result,safe=False)

    def delete(self,request,id):
        server = list(Server.objects.filter(id=id).values())
        if len(server) > 0:
            Server.objects.filter(id=id).delete()
            result = {"result":True}
        else:
            result = {"result":False}
        return JsonResponse(result,safe=False)