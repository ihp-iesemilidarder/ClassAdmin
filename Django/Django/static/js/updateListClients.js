this.onmessage=async(e)=>{
    setInterval(async()=>{
            let res = await fetch("https://classadmin.server/api/clients",{
                method:"GET",
                headers:{
                    "password":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
                    "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
                }
            });
            let data = await res.json();
            this.postMessage(data)
    },2000);
}