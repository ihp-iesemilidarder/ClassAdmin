import os, time
from sources.utils import Environment, Json
from plyer import notification
from tkinter import *
def Notify(title:str,message:str,output=True):
    if(Json(Environment.configuration).print(["notifications"])):
        notification.notify(
            app_name="ClassAdmin",
            app_icon=f"{Environment.media}/images/ClassAdminLogo.ico",
            title=title,
            message=message
        )
    if output:
        text = f"{title}: {message}"
        print(text)
        return text