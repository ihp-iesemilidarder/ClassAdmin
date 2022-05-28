# Author: Ivan Heredia Planas
# ivanherediaplanas@protonmail.com
# Licensed by GNU GENERAL PUBLIC LICENSE VERSION 3
# This file is part of ClassAdmin.
# ClassAdmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# ClassAdmin is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with ClassAdmin. If not, see <https://www.gnu.org/licenses/>.
# Copyright 2022 Ivan Heredia Planas
#
from django.db import models
class Server(models.Model):
    password = models.CharField(max_length=500,null=False)
    ipaddress = models.CharField(max_length=15,null=False)
    port = models.IntegerField(max_length=3,null=False)
    clients = models.IntegerField(max_length=5,null=False)

    class Meta:
        db_table = "server"