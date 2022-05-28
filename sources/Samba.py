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
# This Samba class is used for upload file at shared folder.
#
from sources.utils import logFile, Json, Environment
from sources.Requests import Requests
from smb.SMBConnection import SMBConnection
class Samba:

    @staticmethod
    def upload(filename,path):
        json = Json(Environment.data)
        server = Requests("services","GET","https://classadmin.server/api/servers/1").run().json()["result"]["ipaddress"]
        conn = SMBConnection(str(json.print(["Samba","username"])), str(json.print(["Samba","password"])), str(json.print(["Samba","sharedDirectory"])), str(server), use_ntlm_v2 = True)
        conn.connect(server,139)
        with open(path,"rb") as file:
            conn.storeFile(json.print(["Samba","sharedDirectory"]),filename,file)
        conn.close()