from sources.notification import Notify
from sources.utils import logFile
import threading
class Client:
    def __init__(self,conn,addr):
        try:
            self.conn, self.addr = conn, addr
            self.listenData()
        except (KeyboardInterrupt,SystemExit) as err:
            Notify("showinfo", logFile().message(f"The client {self.addr[0]} left", True, "INFO"))
        except BaseException as err:
            type, object, traceback = sys.exc_info()
            file = traceback.tb_frame.f_code.co_filename
            line = traceback.tb_lineno
            Notify("showerror", logFile().message(f"{err} in {file}:{line}", True, "ERROR"))
        finally:
            try:
                self.conn.close()
            except:
                None

    def listenData(self):
        while True:
            data = self.conn.recv(1024)
            if data:
                raise SystemExit