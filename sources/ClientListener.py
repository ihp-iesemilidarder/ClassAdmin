import signal, os, time, sys, multiprocessing, signal, ssl
from sources.notification import Notify
from sources.listClients import ListClients
from sources.Client import Client
from sources.utils import logFile, Environment
import threading

class ClientListener:
    def __init__(self,conn,addr,event):
        try:
            # Get the connection's socket object and I in this connection add secure traffic encrypted with SSL thanks to object SSLSocket of socket module
            self.addr = addr
            self.conn = self.__SSLTunnel(conn)
            self.nick = ""
            self.__listenData()
        except (KeyboardInterrupt,SystemExit) as err:
            try:
                print(logFile().message(f"The host {self.nick} ({self.addr[0]}:{self.addr[1]}) left :(", True, "INFO"))
            except:
                None
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            print(logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
        finally:
            try:
                #ListClients().remove(self.conn)
                self.conn.close()
            except:
                None
            finally:
                try:
                    Client(self.conn,self.addr).registre(self.nick,"DISCONNECTED",False)
                except:
                    None
                event.set()
                # This will delay 1 second to close the proccess, for this gives time at exitSubprocess method to join the client's child process with the parent process
                time.sleep(1)

    # This creates a ssl tunnel with the ClassAdmin's certificate and private key
    def __SSLTunnel(self,sock):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(Environment.SSL("crt"),Environment.SSL("key"))
        return context.wrap_socket(sock,server_side=True)

    def __listenData(self):
        while True:
            data = self.conn.recv(1024)
            text = data.decode('utf-8')
            if text.startswith("sig."):
                exec(f"raise {text.split('.')[1]}")
            elif data:
                if text.startswith("HelloServer: "):
                    self.nick = text.replace("HelloServer: ","")
                    client = Client(self.conn,self.addr).registre(self.nick, "CONNECTED", False)
                    if client=="sameUser":
                        self.conn.send("sig.SystemExit(-5000,'The nick exists and is connected :(',True)".encode("utf-8"))
                    elif client=="TooManyClients":
                        self.conn.send("sig.SystemExit(-5000,'Too many clients connected. You try it more later',True)".encode("utf-8"))
                    else:
                        print(logFile().message(f"The host {self.nick} ({self.addr[0]}:{self.addr[1]}) is connected :)", True, "INFO"))
                        #ListClients().add(self.conn)
                else:
                    print(data)

    # This method get as argument the process child. For join it at parent process
    @staticmethod
    def exitSubprocess(event,process):
        while True:
            if event.is_set():
                process.join()
                break
            time.sleep(.5)