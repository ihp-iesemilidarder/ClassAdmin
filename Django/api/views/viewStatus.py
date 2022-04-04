import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from sources.django import loginAdmin
from ..models.Status import Status

class viewStatus(View):

    # Avoid the CSRF validate
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if str(request.headers).count("Password") == 0 or str(request.headers).count("Otp") == 0:
            return JsonResponse({"error":"You need authentication with password and otp"})
        elif not loginAdmin(request.headers['password'], request.headers["otp"]):
            return JsonResponse({"error":"Access denied"})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, name=None):
        if name != None:
            status = list(Status.objects.filter(name=name).values())
            if len(status) > 0:
                status = status[0]
            else:
                status = None
        else:
            status = list(Status.objects.values())
            if not len(status) > 0:
                status = None
        return JsonResponse({"result":status},safe=False)

    def post(self, request):
        data = json.loads(request.body)
        Status.objects.create(
            name=data["name"]
        )
        return JsonResponse({"result":True},safe=False)

    def put(self,request,name):
        data = json.loads(request.body)
        status = list(Status.objects.filter(name=name).values())
        if len(status) > 0:
            cursor = connection.cursor()
            cursor.execute("UPDATE status SET name=%s WHERE name=%s", [data["name"],name])
            result = {"result":True}
        else:
            result = {"result":False}
        return JsonResponse(result,safe=False)

    def patch(self,request,name):
        data = json.loads(request.body)
        status = list(Status.objects.filter(id=id).values())
        if len(status) > 0:
            status_object = Status.objects.get(id=id)
            for key in data:
                exec(f"status_object.{key} = data[key]")
            status_object.save()
            result = {"result":True}
        else:
            result = {"result":False}
        return JsonResponse(result,safe=False)

    def delete(self,request,name):
        status = list(Status.objects.filter(name=name).values())
        if len(status) > 0:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM status WHERE name=%s", [name])
            result = {"result":True}
        else:
            result = {"result":False}
        return JsonResponse(result,safe=False)