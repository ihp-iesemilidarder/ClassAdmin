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
# This ClientListener class is used at create the client subprocess.
# And this class is responsible of interact (intermediary) between the client program and server program.
# This sends and receive messages of client and server
#
import time, sys, ssl
from sources.Client import Client
from sources.utils import LogFile, Environment, Notify

class ClientListener:
    def __init__(self,conn,addr,event):
        try:
            # Get the connection's socket object and I in this connection add secure traffic encrypted with SSL thanks to object SSLSocket of socket module
            self.addr = addr
            self.conn = self.__SSLTunnel(conn)
            self.hostname = ""
            self.__listenData()
        except (KeyboardInterrupt,SystemExit):
            try:
                Notify(f"{self.hostname} left", LogFile().message(f"The host {self.hostname} ({self.addr[0]}:{self.addr[1]}) left :(", True, "INFO"))
            except:
                None
        except BaseException as err:
            print(err)
            if err.errno == 104:
                Notify(f"{self.hostname} left unexpected", LogFile().message(f"The host {self.hostname} ({self.addr[0]}:{self.addr[1]}) left unexpected :(", True, "INFO"))
            else:
                type, object, traceback = sys.exc_info()
                file = traceback.tb_frame.f_code.co_filename
                line = traceback.tb_lineno
                Notify("Error", LogFile().message(f"{err} in {file}:{line}", True, "ERROR"))
        finally:
            try:
                self.conn.close()
            except:
                None
            finally:
                try:
                    Client(self.conn,self.addr).registre(self.hostname,"DISCONNECTED")
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

    # This method is the main, is responsible of receive and send data between client/server. Thanks at miniClient/miniServer
    def __listenData(self):
        while True:
            data = self.conn.recv(1024)
            text = data.decode('utf-8')
            if text.startswith("sig."):
                exec(f"raise {text.split('.',1)[1]}")
            elif data:
                if text.startswith("HelloServer: "):
                    self.hostname = text.replace("HelloServer: ","")
                    client = Client(self.conn,self.addr).registre(self.hostname, "CONNECTED")
                    if client=="sameUser":
                        self.conn.send("sig.SystemExit(-5000,'The hostname exists and is connected :(',True)".encode("utf-8"))
                    elif client=="TooManyClients":
                        self.conn.send("sig.SystemExit(-5000,'Too many clients connected. You try it more later',True)".encode("utf-8"))
                    else:
                        Notify(f"{self.hostname} connected", LogFile().message(f"The host {self.hostname} ({self.addr[0]}:{self.addr[1]}) is connected :)", True, "INFO"))
                else:
                    print(data)
            elif len(data)==0:
                raise SystemExit

    # This method get as argument the process child. For join it at parent process. This delete the subprocess at end.
    @staticmethod
    def exitSubprocess(event,process):
        while True:
            if event.is_set():
                process.join()
                break
            time.sleep(.5)