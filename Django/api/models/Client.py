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

class Client(models.Model):
    hostname = models.CharField(max_length=50,null=False)
    ipaddress = models.CharField(max_length=15,null=False)
    port = models.IntegerField(max_length=5,null=False)
    status = models.CharField(max_length=50,null=False)
    server = models.CharField(max_length=50,null=False,db_column="cli_ser_id")

    class Meta:
        db_table = "clients"
        constraints = [
            # CONSTRAINT `ser_port_CK` CHECK (`port` between 0 and 65535)
            models.CheckConstraint(
                check=models.Q(port__gte=0) & models.Q(port__lte=65535),
                name="cli_port_CK"
            ),

            # CONSTRAINT `ser_ipaddress_REGEXP` CHECK (`ipaddress` regexp '^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$')
            models.CheckConstraint(
                check=models.Q(
                    ipaddress__iregex=r'^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$'
                ),
                name="cli_ipaddress_REGEXP"
            ),
        ]