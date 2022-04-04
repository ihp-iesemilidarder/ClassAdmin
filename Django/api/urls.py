from django.urls import path

from .views.viewStatus import viewStatus
from .views.viewClient import viewClient
from .views.viewServer import viewServer

urlpatterns=[
    path("status",viewStatus.as_view()),
    path("status/<str:name>",viewStatus.as_view()),

    path("clients", viewClient.as_view()),
    path("clients/<int:id>", viewClient.as_view()),
    path("clients/<str:id>",viewClient.as_view()),
    # Find client by address or nick
    path("clients/<str:address>/<str:nick>", viewClient.as_view()),

    path("servers", viewServer.as_view()),
    path("servers/<int:id>", viewServer.as_view())
]