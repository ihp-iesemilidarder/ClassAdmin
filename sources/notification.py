import tkinter as tk
from tkinter import messagebox

def Notify(type:str,text:str,output=True):
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    exec(f'messagebox.{type}("NotiClass", "{text}")')
    root.destroy()
    if output:
        print(text)