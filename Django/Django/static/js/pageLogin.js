/*
 Author: Ivan Heredia Planas
 ivanherediaplanas@protonmail.com
 Licensed by GNU GENERAL PUBLIC LICENSE VERSION 3
 This file is part of ClassAdmin.
 ClassAdmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 ClassAdmin is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 You should have received a copy of the GNU General Public License along with ClassAdmin. If not, see <https://www.gnu.org/licenses/>.
 Copyright 2022 Ivan Heredia Planas
*/
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