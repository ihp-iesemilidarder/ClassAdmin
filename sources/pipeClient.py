#!/usr/bin/python3
import os,socket,sys,time,urllib3
import ssl
from base64 import b64encode
from sources.Requests import Requests
# This socket clint is used for comunicate with the clients
from sources.utils import Environment


class PipeClient:
    def __init__(self,ipaddress):
        urllib3.disable_warnings()
        self.ipaddress = ipaddress
        self.__SSLTunel()
        self.__createSocket()
        self.__handlerPipeServer()

    # This creates a ssl tunnel with the ClassAdmin's certificate and private key
    def __SSLTunel(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations(Environment.CA)

    def __createSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sockSSL = self.context.wrap_socket(sock, server_hostname="classadmin.server")
        self.sockSSL = ssl.create_default_context().wrap_socket(sock, server_hostname="classadmin.server")

    def __handlerPipeServer(self):
        while True:
            try:
                PORT = int(
                    Requests("services", "GET", "https://classadmin.server/api/servers").run().json()["result"][0][
                        "port"])
                # connection at server (without specified ip ipaddress), so if the server changes the ip ipaddress,
                # the client will can connect.
                self.sockSSL.connect((self.ipaddress, PORT))
                break
            except BaseException as err:
                try:
                    if err.args[0] != 10061 and sys.platform.system().upper() == "WINDOWS":
                        os.system(f"taskkill /PID {os.getpid()} /F")
                    else:
                        pass
                except:
                    pass
            time.sleep(.5)

    def send(self,data):
        self.sockSSL.send(data.encode("utf-8"))
        time.sleep(1)
        self.sockSSL.close()