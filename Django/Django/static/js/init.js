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
import './lib/sha512.js';
const mess = document.querySelector("div#message");

export async function enterSession(){
    let res = await fetch("/api/servers",{
        method:"GET",
        headers:{
            password:",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(",
            otp:",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
        }
    });
    let data = await res.json();
    let password = sha512(data["result"][0]["password"]);
    if (localStorage.getItem("sessionToken")!=null && localStorage.getItem("sessionToken")==password && location.pathname=='/'){
        location.href='dashboard';
    }else if((localStorage.getItem("sessionToken")==null || getCookie("sessionToken")==null || localStorage.getItem("sessionToken")!=password) && location.pathname=='/dashboard/'){
        localStorage.removeItem("sessionToken");
        location.href='/';
    }
}

export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function messg(msg,type=bool){
    mess.innerText=msg;
    if(type){
        mess.style.background="rgb(63, 226, 25)";
        mess.style.color='black';
    }else{
        mess.style.background="rgb(226, 25, 25)";
        mess.style.color='white';
    }
    mess.animate([
        {bottom:'0'}
    ],{
        duration:1000
    });
    setTimeout(()=>{
        mess.style.bottom="0";
    },1000);
    setTimeout(()=>{
        mess.animate([
            {bottom:'-100%'}
        ],{
            duration:1000
        });
        setTimeout(()=>{
            mess.removeAttribute("style");
        },1000);
    },3000);
}