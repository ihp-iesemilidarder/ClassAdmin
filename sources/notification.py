import os, time
from sources.utils import Environment, Json
from notifypy import Notify as notify
def Notify(title:str,message:str,output=True):
    if(Json(Environment.configuration).print(["notifications"])):
        notification = notify()
        notification.title = title
        notification.message = message
        notification.icon = f"{Environment.media}/images/ClassAdminLogo.png"
        notification.send()
    if output:
        text = f"{title}: {message}"
        print(text)
        return text