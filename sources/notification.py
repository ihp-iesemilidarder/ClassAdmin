from sources.utils import Environment, Json
def Notify(title:str,message:str,output=True):
    if(Json(Environment.configuration).print(["notifications"])):
        try:
            from notifypy import Notify as notify
            notification = notify()
            notification.title = title
            notification.message = message
            notification.icon = f"{Environment.media}/images/ClassAdminLogo.png"
            notification.send()
        except:
            None
    if output:
        text = f"{title}: {message}"
        print(text)
        return text