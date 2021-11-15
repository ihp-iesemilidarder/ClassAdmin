import os, time
from sources.utils import Environment
from tkinter import messagebox
from tkinter import *
def Notify(type:str,text:str,output=True):
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    exec(f'messagebox.{type}("NotiClass", "{text}")')
    root.destroy()
    if output:
        print(text)
        return text