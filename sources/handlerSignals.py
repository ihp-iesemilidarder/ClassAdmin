import os,time,signal
class HandlerSignals:
    def __init__(self):
        signal.signal(signal.SIGTERM,self.shutdown)
    def shutdown(self,code,msg):
        raise SystemExit