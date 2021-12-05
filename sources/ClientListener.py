import signal, os, time, sys, multiprocessing, signal
from sources.notification import Notify
from sources.listClients import ListClients
from sources.Client import Client
from sources.utils import logFile
import threading

class ClientListener:
    def __init__(self,conn,addr,event):
        try:
            self.conn, self.addr = conn, addr
            self.nick = ""
            self.__listenData()
        except (KeyboardInterrupt,SystemExit) as err:
            print(logFile().message(f"The host {self.nick} ({self.addr[0]}:{self.addr[1]}) left", True, "INFO"))
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            print(logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
        finally:
            try:
                ListClients().remove(self.conn)
                self.conn.close()
            except:
                None
            finally:
                Client(self.conn,self.addr).registre(self.nick,"DISCONNECTED",False)
                event.set()
                # This will delay 1 second to close the proccess, for this gives time at exitSubprocess method to join the client's child process with the parent process
                time.sleep(1)
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
                    if client==False:
                        self.conn.send(b"sig.SystemExit(-5000,'The nick exists and is connected',True)")
                    else:
                        print(logFile().message(f"The host {self.nick} ({self.addr[0]}:{self.addr[1]}) is connected", True, "INFO"))
                        ListClients().add(self.conn)
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