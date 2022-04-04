this.onmessage=async(e)=>{
    setInterval(async()=>{
            let res = await fetch("https://classadmin.server/dashboard/",{
                method:"POST",
                body:"action=keepAlive",
                headers:{
                    "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                    "X-CSRFToken":e.data[0]
                }
            });
            let data = await res.json();
            this.postMessage(data)
    },3000);
}