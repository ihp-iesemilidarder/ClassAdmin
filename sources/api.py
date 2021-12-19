from sources.django import loginAdmin, logFile
import sqlite3,re,mariadb
from django.urls import  path
from django.http import JsonResponse, HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

"""
==========================API REST==========================
 SYNTAX:
    127.0.0.1/api[/table,table1,table3,...][/column]?<key>=[>|<|>=|<=]<value>&[|]<key>=[>|<|>=|<=]<value>&LIMIT=<min>[,max]
============================================================
 IMPORTANT:
    For do a request you need authentication with password and OTP

 EXAMPLES:
    GET:
        127.0.0.1/api/server -> SELECT * FROM server
        127.0.0.1/api/server?LIMIT=5 -> SELECT * FROM server LIMIT 5
        127.0.0.1/api/server?password=ejem&id=1&LIMIT=5,7 -> SELECT * FROM server WHERE password='ejem' AND id=1 LIMIT 5,7
        127.0.0.1/api/server/password,status -> SELECT password,status FROM server
        127.0.0.1/api/server/password?id=1&password=hola -> SELECT password FROM server WHERE id=1 AND password='hola'
        127.0.0.1/api/server/password?id=1&|password=hola -> SELECT password FROM server WHERE id=1 OR password='hola'
        
    POST:
        127.0.0.1/api/server -> INSERT INTO server (otp,ejem) VALUES (1234,'1233da')
            Body x-www-form-urlencoded
                key     value
                --------------------
                otp     1234
                ejem    1233da
                
        IMPORTANT: The params in the url doesn't affect
        
    PUT:
        127.0.0.1/api/server?port=8899&|password=h -> UPDATE server SET otp='1234', ejem='1233da' WHERE port=8899 OR password='h'
            Body x-www-form-urlencoded
                key     value
                --------------------
                otp     1234
                ejem    1233da
                
    DELETE:
        127.0.0.1/api/server?port=8899&password=h -> DELETE FROM server WHERE port=8899 AND password='h'
            not body data
"""

class getData:
    def __init__(self,data):
        self.list = QueryDict(data)
        self.output = ''

    # This method returns key1,key2,key3...
    # For clause as SELECT, INSERT
    def getKeys(self):
        for t in self.list:
            self.output+=f'{t},'
        self.output = re.sub(r",$","",self.output)
        return self.output

    # This method returns value1,value2,value3...
    # For clause as SELECT, INSERT
    def getValues(self):
        for t in self.list:
            try:
                if int(self.list[t]):
                    self.output+=f'{self.list[t]},'
            except:
                self.output += f"'{self.list[t]}',"
        self.output = re.sub(r",$","",self.output)
        return self.output

    # This method returns key1=value1, key2=value2, key3=value3
    # being '=' the 'delimitator'
    # For clause as UPDATE
    def keysValues(self,delimitator):
        for value in self.list:
            self.output+=f"{value}{delimitator}'{self.list[value]}', "
        self.output = re.sub(r", $", "", self.output)
        return self.output

class API:
    # if there are columns, show it
    def columns(self,columns):
        if columns:
            return  columns
        else:
            return "*"

    # This method add the operator specified in the url
    def keyWhere(self,key):
        operator = re.sub(r"[^>|<|=]","",key)
        value = re.sub(r"[>|<|=]","",key)
        if operator == "":
            operator="="
        try:
            if int(value):
                return f"{operator}{value}"
        except:
            return f"{operator}'{value}'"

    def LimitClause(self,params):
        if params:
            output = ''
            for key in params:
                if key=="LIMIT":
                    output=f" LIMIT {params[key]}"
            return output
        else:
            return ""

    # This method add AND or OR in each condition in WHERE
    def WhereClause(self,params):
        if params:
            output=''
            for key in params:
                if key=="LIMIT":
                    continue
                operator = "OR" if key[0]=="|" else "AND"
                if list(params).index(key) > 0:
                    output+=f" {operator} {key[1::] if operator=='OR' else key}{self.keyWhere(params[key])}"
                else:
                    output += f"WHERE {key[1::] if operator=='OR' else key}{self.keyWhere(params[key])}"
            return output
        else:
            return ""

    @csrf_exempt
    def requests(self,req,table:str,columns:list=False):
        try:
            if str(req.headers).count("Password")==0 or str(req.headers).count("Otp")==0:
                raise Exception("You need authentication with password and otp")
            elif not loginAdmin(req.headers['password'], req.headers["otp"]):
                raise Exception("Access denied")
            conn = mariadb.connect(
                host="127.0.0.1",
                user="ClassAdmin",
                password="12345678",
                database="ClassAdmin"
            )
            cursor = conn.cursor()
            if req.method == "GET":
                cursor.execute(f"SELECT {self.columns(columns)} FROM {table} {self.WhereClause(req.GET.dict())}{self.LimitClause(req.GET.dict())}")
                data = cursor.fetchall()
                rows = cursor.column_names
                results = []
                conn.close()
                for item in range(len(data)):
                    obj=dict({})
                    for row in range(len(rows)):
                        print(f"obj['{row}']=data[{item}]['{row}']")
                        print(obj)
                        print(data)
                        obj[str(rows[row])]=data[item][row]
                    results.append(obj)
                if len(data) == 0:
                    results = None
                return JsonResponse({
                    "result": results
                })
            elif req.method == "POST":
                if columns:
                    raise Exception("POST not allowed")
                cursor.execute(f"INSERT INTO {table} ({getData(req.body).getKeys()}) VALUES ({getData(req.body).getValues()})")
                conn.commit()
                conn.close()
                return JsonResponse({"result":True})
            elif req.method == "PUT":
                if columns:
                    raise Exception("PUT not allowed")
                cursor.execute(f"UPDATE {table} SET {getData(req.body).keysValues('=')} {self.WhereClause(req.GET.dict())}")
                conn.commit()
                conn.close()
                return JsonResponse({"result": True})
            elif req.method == 'DELETE':
                if columns:
                    raise Exception("DELETE not allowed")
                cursor.execute(f"DELETE FROM {table} {self.WhereClause(req.GET.dict())}")
                conn.commit()
                conn.close()
                return JsonResponse({"result": True})
        except BaseException as err:
            ## the err.msg and err.errno aren't exist if the exception is throw by a raise
            try:
                message = err.msg
                code = err.errno
            except:
                message = err
                code = -5001
        finally:
            try:
                try:
                    return JsonResponse({"code":code,"message":f"{logFile(True).message(message,True)}"})
                except BaseException as err:
                    return JsonResponse({"code": code, "message": f"{err}"})
            except:
                None
urlpatterns=[
    path('<table>',API().requests),
    path('<table>/<columns>',API().requests)
]