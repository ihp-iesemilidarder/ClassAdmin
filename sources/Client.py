import multiprocessing, signal, os, threading
from sources.notification import Notify
from sources.utils import logFile
import threading
class Client:
    def __init__(self,conn,addr):
        try:
            self.conn, self.addr = conn, addr
            print(logFile().message(f"Client {self.addr[0]} connected by port {self.addr[1]}", True, "INFO"))
            self.listenData()
        except (KeyboardInterrupt,SystemExit) as err:
            print(logFile().message(f"The client {self.addr[0]} left", True, "INFO"))
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            print(logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
        finally:
            try:
                self.conn.close()
            except:
                None

    def listenData(self):
        while True:
            data = self.conn.recv(1024)
            text = data.decode('utf-8')
            if text.startswith("sig."):
                exec(f"raise {text.split('.')[1]}")
            elif data:
                print(data)