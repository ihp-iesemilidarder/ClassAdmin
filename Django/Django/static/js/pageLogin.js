import {messg,getCookie,enterSession} from './init.js';
import './lib/sha512.js';
const loginButton = document.querySelector("#pageLogin form input[type='button']");
const form = document.querySelector("#pageLogin form");
const otpField = document.querySelector("#pageLogin form input#twoFA");
const checkRecoveryCodes = document.querySelector("#pageLogin form input[type='checkbox']");

const recoveryCodes=(e)=>{
    if(checkRecoveryCodes.checked){
        otpField.setAttribute("name","recoveryCodes");
        otpField.setAttribute("placeholder","recovery code");
    }else{
        otpField.setAttribute("name","otp");
        otpField.setAttribute("placeholder","code OTP");
    }
}

const validateData=(data)=>{
    if(isNaN(data.get("otp")) || data.get("password")==''){
        return false;
    }
    return true;
}

async function login(e){
    try{
        e.preventDefault();
        let formData = new FormData(form);
        if(!validateData(formData)){
            throw new Error("The fields are required and the OTP should be numeric");
        }
        let res = await fetch("./",{
            method:"POST",
            body:formData,
            headers:{
                "X-CSRFToken": getCookie('csrftoken'),
                "X-Requested-With":"XMLHttpRequest"
            }
        });
        let data = await res.json();
        if(data.login==true){
            messg("Login successful",true);
            let token = sha512(sha512(formData.get("password")));
            localStorage.setItem("sessionToken",token);
            document.cookie = `sessionToken=; max-age=3600`;
            location.href='dashboard';
        }else if(data.login==false){
            messg("Login failed",false);
        }else{
            messg(data.login,false);
        }
    }catch(error){
        messg(`Error unexpected: ${error}`,false);
    }
}

export async function pageLogin(){
    document.querySelector("body").style.backgroundImage="url(/static/images/wallpaper.png)";
    loginButton.addEventListener("click",await login);
    checkRecoveryCodes.addEventListener("click",recoveryCodes);
    enterSession();
}