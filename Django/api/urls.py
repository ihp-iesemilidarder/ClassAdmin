# Author: Ivan Heredia Planas
# ivanherediaplanas@protonmail.com
# Licensed by GNU GENERAL PUBLIC LICENSE VERSION 3
# This file is part of ClassAdmin.
# ClassAdmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# ClassAdmin is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with ClassAdmin. If not, see <https://www.gnu.org/licenses/>.
# Copyright 2022 Ivan Heredia Planas
#
# This show the API endpoints
#
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
    # Find client by ipaddress or hostname
    path("clients/<str:ipaddress>/<str:hostname>", viewClient.as_view()),

    path("servers", viewServer.as_view()),
    path("servers/<int:id>", viewServer.as_view())
]