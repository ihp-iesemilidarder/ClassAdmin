import {messg,getCookie} from './init.js';

export const editUser=async(e)=>{
    let node = e.target;
    let id = node.parentNode.parentNode.parentNode.dataset.id;
    let nick = node.parentNode.parentNode.querySelector("form input#nick").value;
    try{
        let request = await fetch("./",{
            method:"POST",
            body:`action=editNickname&id=${id}&nick=${nick}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json()
        if(data.result){
            messg(`nickname edited successfully to ${nick}`,true);
        }else{
            messg("Error at edit the nickname",false);
        }
    }catch(error){
        messg(`Unexpected error at edit nickname: ${error}`,false);
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