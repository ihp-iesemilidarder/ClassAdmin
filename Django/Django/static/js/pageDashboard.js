import './lib/sha512.js';
import './lib/FileSaver.js';
import {enterSession, messg, getCookie} from './init.js';
const buttonConf = document.querySelector("#pageDashboard .fa-cog");
const closeConf = document.querySelector("#pageDashboard #config .fa-close");
const saveConf = document.querySelector("#pageDashboard #config input[type='submit']");
const formConf = document.querySelector("#pageDashboard #config form");
const newOTP = document.querySelector('#pageDashboard #config .fa-plus');
const imgQR = document.querySelector('#pageDashboard #config img');
const buttonLogout = document.querySelector('#pageDashboard .fa-sign-out-alt');
const buttonDownloadRecoveryCodes = document.querySelector("#pageDashboard #config form #action a");

const sessionLogout=()=>{
    localStorage.removeItem("sessionToken");
    messg("session closed",true);
}

async function reloadOTP(){
    try{
        let res = await fetch(".",{
            method:"POST",
            body:"action=newOTP",
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await res.json();
        if(data.result!=false){
            imgQR.src = data.result;
            messg("QR code reloaded",true);
        }else{
            messg("Error at reload QR code",false);
        }
    }catch(err){
        messg(`Error during the OTP reload: ${err}`,false);
    }
}

async function sendConfig(data){
    try{
        let bodyData = `password=${sha512(data.get("newPassword"))}&port=${parseInt(data.get("port"))}`;
        let res = await fetch("/api/server?id=1",{
            method:"PUT",
            body:bodyData,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "password":data.get("currentPassword"),
                "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
            }
        });
        let json = await res.json();
        if(json["result"]){
             messg("Configuration updated sucessfully",true);
             await cookie()
        }else{
            throw json;
        }
    }catch(err){
        if(err["code"]==2003){
            messg("Connection at database failed",false);
        }else{
            messg(`Error unexpected: ${err.message}`,false);
        }
    }
}

const validateConf=(data)=>{
    if(data.get("currentPassword").length==0 || data.get("newPassword").length==0 || data.get("againNewPassword").length==0 || data.get("port").length==0){
        messg("There are fields empties",false);
        return false;
    }else if(data.get("newPassword")!=data.get("againNewPassword")){
        messg("The passwords aren't match",false);
        return false;
    }else if(isNaN(data.get("port"))){
        messg("The port must be number",false);
        return false;
    }else if(data.get("port") < 1024 || data.get("port") > 65535){
        messg("The port must be between 1024 and 65535",false);
        return false;
    }
    return true;
}

async function saveConfig(e){
    e.preventDefault();
    let data = new FormData(formConf);
    if(validateConf(data)){
        await sendConfig(data);
    }
}

async function cookie(){
    let res = await fetch("/api/server/password",{
        method:"GET",
        headers:{
            password:",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            otp:",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        }
    });
    let data = await res.json();
    let password = sha512(data["result"][0]["password"]);
    setInterval(()=>{
        if (localStorage.getItem("sessionToken")!=null && localStorage.getItem("sessionToken")==password && location.pathname=='/'){
            location.href='dashboard';
        }else if((localStorage.getItem("sessionToken")==null || getCookie("sessionToken")==null || localStorage.getItem("sessionToken")!=password) && location.pathname=='/dashboard/'){
            localStorage.removeItem("sessionToken");
            location.href='/';
        }
    },1000);
}

const keepAliveServer=()=>{
    let thread = new Worker('/static/js/keepAliveServer.js');
    thread.postMessage([getCookie("csrftoken")])
    thread.onmessage=(e)=>{
        document.querySelector("#pageDashboard").style=`border:15px solid #${(e.data.result)?"008037":"747373"}`;
    }
}

export async function pageDashboard(){
    buttonConf.addEventListener("click",()=>config.style.right="0");
    closeConf.addEventListener("click",()=>config.removeAttribute("style"));
    enterSession();
    await cookie();
    saveConf.addEventListener("click",await saveConfig);
    newOTP.addEventListener("click",await reloadOTP);
    buttonLogout.addEventListener("click", sessionLogout);
    keepAliveServer()
}