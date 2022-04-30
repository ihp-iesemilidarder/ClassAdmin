import {messg,getCookie} from './init.js';

export const editHostName=async(e)=>{
    let node = e.target;
    let id = node.parentNode.parentNode.parentNode.dataset.id;
    let hostname = node.parentNode.parentNode.querySelector("form input#hostname").value;
    try{
        let request = await fetch("./",{
            method:"POST",
            body:`action=editHostName&id=${id}&hostname=${hostname}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json()
        if(data.result){
            messg(`hostname edited successfully to ${hostname}`,true);
        }else{
            messg("Error at edit the hostname",false);
        }
    }catch(error){
        messg(`Unexpected error at edit hostname: ${error}`,false);
    }
}

export const shutdownComputer=async(node)=>{
    let id = node.parentNode.parentNode.dataset.id;
    try{
        let request = await fetch("./",{
            method:"POST",
            body:`action=shutdownHost&id=${id}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json()
        if(data.result){
            messg("Computer powered off successfully",true);
        }else{
            messg("Error at power off the computer",false);
        }
    }catch(error){
        messg(`Unexpected error at power off the computer: ${error}`,false);
    }
}

export const rebootComputer=async(node)=>{
    let id = node.parentNode.parentNode.dataset.id;
    try{
        let request = await fetch("./",{
            method:"POST",
            body:`action=rebootHost&id=${id}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json()
        if(data.result){
            messg("Computer restarted successfully",true);
        }else{
            messg("Error at restart the computer",false);
        }
    }catch(error){
        messg(`Unexpected error at restart the computer: ${error}`,false);
    }
}
export const suspendComputer=async(node)=>{
    let id = node.parentNode.parentNode.dataset.id;
    try{
        let request = await fetch("./",{
            method:"POST",
            body:`action=suspendHost&id=${id}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json()
        if(data.result){
            messg("the computer suspended successfully",true);
        }else{
            messg("Error at suspend the computer",false);
        }
    }catch(error){
        messg(`Unexpected error at suspend the computer: ${error}`,false);
    }
}
export const sendAlert=async(node,type,title,description)=>{
    let id = node.parentNode.parentNode.parentNode.dataset.id;
    try{
        let request = await fetch("./",{
            method:"POST",
            body:`action=sendAlert&id=${id}&type=${type}&title=${title}&description=${description}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json()
        if(data.result){
            messg("The alert has been sent at client successfully",true);
        }else{
            messg("Error at send the alert at client",false);
        }
    }catch(error){
        messg(`Unexpected error at send a alert at computer: ${error}`,false);
    }
}

export const screenshot=async(node)=>{
    try{
        let id = node.parentNode.parentNode.dataset.id;
        let request = await fetch("./",{
            method:"POST",
            body:`action=screenshot&id=${id}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json()
        if(data.result){
            messg("The client desktop has been captured successfully",true);
        }else{
            messg("Error at capture the client desktop",false);
        }
    }catch(error){
        messg(`Unexpected error at capture the client desktop: ${error}`,false);
    }
}

export const listPrograms=async(node)=>{
    try{
        let id = node.parentNode.parentNode.dataset.id;
        let request = await fetch("./",{
            method:"POST",
            body:`action=listPrograms&id=${id}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json()
        if(data.result){
            document.querySelector("#pageDashboard div#listPrograms").style.display="flex";
        }else{
            messg("Error at load the client computer programs",false);
        }
    }catch(error){
        messg(`Unexpected error at capture the client desktop: ${error}`,false);
    }
}