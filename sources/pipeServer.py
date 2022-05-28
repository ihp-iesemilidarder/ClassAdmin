#!/usr/bin/python3
# Author: Ivan Heredia Planas
# 2 CFGS ASIX
#
# This pipServer class is used for listen the data sent by the pipeClient.
# This class is used in each client button of Django app.
#
import time,socket,ssl,urllib3,sys
from sources.Requests import Requests
from sources.utils import Environment, Notify, logFile
from sources.eventsClient import EventsClient

class PipeServer:
    def __init__(self,event):
        try:
            urllib3.disable_warnings()
            self.port = Requests("services","GET","https://classadmin.server/api/servers").run().json()["result"][0]["port"]
            self.__createSocket()
            self.__SSLTunnel()
            self.__handlerClient()
        except (KeyboardInterrupt, SystemExit,GeneratorExit) as err:
            pass
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            Notify("Error",logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
        finally:
            try:
                self.sockSSL.close()
                event.set()
            except:
                None
    # this listen the client connected puntually and his data
    def __handlerClient(self):
        while self.sockSSL:
            self.conn,self.addr = self.sockSSL.accept()
            self.__handlerMessages()
            time.sleep(.5)

    def __handlerMessages(self):
        while self.conn:
            data = self.conn.recv(1048576)
            text = data.decode('utf-8')
            if len(data)>0:
                EventsClient().run(text)
                self.conn.close()
                break
            elif len(data)==0:
                self.conn.close()
            time.sleep(1)


    # This creates a ssl tunnel with the ClassAdmin's certificate and private key
    def __SSLTunnel(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(Environment.SSL("crt"),Environment.SSL("key"))
        self.sockSSL = context.wrap_socket(self.sock,server_side=True)

    @staticmethod
    def close(process,event):
        while True:
            if event.is_set():
                process.join()
                break
            time.sleep(.5)

    def __createSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("",self.port+5))
        self.sock.listen(1)