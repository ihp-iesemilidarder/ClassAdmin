import requests
from sources.utils import Environment
def clientRegistre(nick,address,port,status):
    client = requests.get(f"https://classadmin.server/api/clients?address={address}&nick={nick}",headers={
            "password": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            "otp": ",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
    },verify="/etc/ssl/certs/ca-certificates.crt").json()["result"]
    if client==None:
        requests.post(f"https://classadmin.server/api/clients",
            headers={
                "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            },
            data=f"nick={nick}&address={address}&port={port}&status={status}&cli_ser_id=1",
            verify="/etc/ssl/certs/ca-certificates.crt"
        )
    else:
        requests.put(f"https://classadmin.server/api/clients?nick={nick}",
            headers={
                "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            },
            data=f"nick={nick}&address={address}&port={port}&status={status}&cli_ser_id=1",
            verify="/etc/ssl/certs/ca-certificates.crt"
        )