import requests
from sources.utils import Environment
def clientRegistre(nick,address,port,status):
    client = requests.get(f"https://{address}/api/clients/?address={address}&port={port}",headers={
        "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
        "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
    },cert=(f"/etc/ClassAdmin/ssl/ClassAdmin1.crt", f"/etc/ClassAdmin/ssl/ClassAdmin1.key")).json()[0]["result"]
    if client==None:
        requests.post(f"https://{address}/api/clients/",
            headers={
                "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            },
            body=f"nick={nick}&address={address}&port={port}&status={status}&cli_ser_id=1",
            certs=("/etc/ClassAdmin/ssl/ClassAdmin1.crt","/etc/ClassAdmin/ssl/ClassAdmin1.key")
        )
    else:
        requests.put(f"https://{address}/api/clients/",
            headers={
                "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            },
            body=f"nick={nick}&address={address}&port={port}&status={status}&cli_ser_id=1",
            cert=(f"/etc/ClassAdmin/ssl/ClassAdmin1.crt", f"/etc/ClassAdmin/ssl/ClassAdmin1.key")
        )