import './lib/sha512.js';
import './lib/FileSaver.js';
import {enterSession, messg, getCookie} from './init.js';
import {editHostName,shutdownComputer,rebootComputer,suspendComputer,sendAlert,screenshot,listPrograms,printListPrograms} from "./eventsClients.js";
const buttonConf = document.querySelector("#pageDashboard .fa-cog");
const closeConf = document.querySelector("#pageDashboard #config .fa-close");
const saveConf = document.querySelector("#pageDashboard #config input[type='submit']");
const formConf = document.querySelector("#pageDashboard #config form");
const newOTP = document.querySelector('#pageDashboard #config .fa-plus');
const imgQR = document.querySelector('#pageDashboard #config img');
const buttonLogout = document.querySelector('#pageDashboard .fa-sign-out-alt');
const buttonDownloadRecoveryCodes = document.querySelector("#pageDashboard #config form #action a");
const containerClients = document.querySelector(".clients");
const checkboxNotification = document.querySelector("#pageDashboard #notificationDiv input");
const currentPort = document.querySelector("#pageDashboard #currentPort span");
const currentUserNotification = document.querySelector("#pageDashboard #currentUserNotification span");
const buttonUserNotification = document.querySelector("#pageDashboard #config #saveUserNotification");
const inputUserNotification = document.querySelector("#pageDashboard #config input[name='userNotification']");
const containerFormEdit = document.querySelector("#pageDashboard #formEditUser");
const containerFormNotification = document.querySelector("#pageDashboard #formNotification");
// file uploader
const containerUploadFiles = document.querySelector("#pageDashboard div#containerUploadFile");
const inputUploadFiles = document.querySelector("#pageDashboard div#containerUploadFile input#uploadFile");
const closeUploadFiles = document.querySelector("#pageDashboard div#containerUploadFile i.fa-circle-xmark");
let files;
// listPrograms div
const containerListPrograms = document.querySelector("#pageDashboard div#listPrograms")

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

// save the data in the DB (port or password)
async function sendConfigDB(data){
    try{
        let bodyData = {
            password:sha512(data.get("newPassword")),
            port:parseInt(data.get("port"))
        }
        if(data.get("newPassword").length==0){
            bodyData = {
                port:parseInt(data.get("port"))
            }
        }else if(data.get("port").length==0){
            bodyData = {
                password: sha512(data.get("newPassword"))
            }
        }
        console.log(bodyData)
        let res = await fetch("/api/servers/1",{
            method:"PATCH",
            body:JSON.stringify(bodyData),
            headers:{
                "Content-Type":"application/json;charset=UTF-8",
                "password":(data.get("currentPassword").length!=0)?data.get("currentPassword"):",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS(", // for validate if the user is authorized
                "otp":",UPsz)ZfF~ZOh^:YH)o[4P<sF7$jS("
            }
        });
        let json = await res.json();
        if(json.result==true){
             messg("Configuration updated sucessfully",true);
             await cookie()
        }else{
            throw json;
        }
    }catch(err){
        messg(`Error unexpected: ${err.error}`,false);
    }
}

const validateConfDB=(data)=>{
    let passwords = [data.get("currentPassword"),data.get("newPassword"),data.get("againNewPassword")]
    // There are some fields passwords empties but not all
    if((data.get("currentPassword").length==0 || data.get("newPassword").length==0 || data.get("againNewPassword").length==0) &&
        (data.get("currentPassword").length!=0 || data.get("newPassword").length!=0 || data.get("againNewPassword").length!=0)){
        messg("There are fields for change the password are empties",false);
        return false;
    }else if(data.get("newPassword")!=data.get("againNewPassword")){
        messg("The passwords aren't match",false);
        return false;
    }else if(data.get("port").length!=0 && isNaN(data.get("port"))){
        messg("The port must be number",false);
        return false;
    }else if(data.get("port").length!=0 && (data.get("port") < 1024 || data.get("port") > 65535)){
        messg("The port must be between 1024 and 65535",false);
        return false;
    }else if(data.get("currentPassword").length==0 && data.get("newPassword").length==0 && data.get("againNewPassword").length==0 && data.get("port").length==0){
        messg("The fields are empties",false);
        return false;
    }
    return true;
}

async function saveConfig(e){
    e.preventDefault();
    let data = new FormData(formConf);
    if(validateConfDB(data)){
        await sendConfigDB(data);
    }
}

async function cookie(){
    let res = await fetch("/api/servers",{
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

const drawListClients=(list)=>{
    containerClients.innerHTML="";
    if(list.result==null) return false;
    list.result.forEach(list=>{
        containerClients.innerHTML+=`
            <div data-id="${list.id}" class="client">
                <div class="info">
                    <img src="/static/images/logoUser.png" alt="logo">
                    <span class="hostname">${list.hostname}</span>
                    <span title="ip address">${list.ipaddress}</span>
                    <span title="port">${list.port}</span>
                </div>
                <div class="actions">
                    <i class="fa fa-trash" title="delete" aria-hidden="true"></i><span class="sr-only">delete</span>
                    <i class="fa fa-user-pen" title="edit hostname" aria-hidden="true"></i>
                    <i class="fa fa-redo" title="reboot computer" aria-hidden="true"></i>
                    <i class="fa fa-power-off" title="shutdown computer" aria-hidden="true"></i>
                    <i class="fa fa-moon" title="suspend computer" aria-hidden="true"></i>
                    <i class="fa fa-ban" title="deny programs" aria-hidden="true"></i>
                    <i class="fa fa-camera" title="screenshot" aria-hidden="true"></i>
                    <i class="fa fa-bell" title="send alert" class="send-alert"></i>
                    <i class="fa fa-upload" title="upload file" class="send-message"></i>
                    <i class="fa fa-wifi ${list.status}" title="status" aria-hidden="true"></i>
                </div>
            </div>
        `;
    })

}

const showAliveServer=()=>{
    let thread = new Worker('/static/js/showAliveServer.js');
    thread.postMessage([getCookie("csrftoken")]);
    thread.onmessage=(e)=>{
        document.querySelector("#pageDashboard").style=`border:15px solid #${(e.data.result)?"008037":"747373"}`;
    }
}

const updateListClients=()=>{
    let thread = new Worker("/static/js/updateListClients.js");
       thread.postMessage([getCookie("csrftoken")]);
       thread.onmessage=(e)=>{
        drawListClients(e.data);
       }
}

const activeDisableNotifications=async()=>{
    let request = await fetch(".",{
        method:"POST",
        headers:{
            "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
            "X-CSRFToken":getCookie("csrftoken")
        },
        body:"notifications="+checkboxNotification.checked
    });
    let status = await request.json();
    if(status.result){
        messg("The settings of the notifications were changed",true);
    }else{
        messg("Error during the change of the settings of the notifications",false);
    }
}

const showAliveData=()=>{
    let thread = new Worker('/static/js/showAliveData.js');
    thread.postMessage([getCookie("csrftoken")]);
    thread.onmessage=(e)=>{
        currentPort.innerText = e.data.result.port;
        currentUserNotification.innerText = e.data.result.userNotification;
        checkboxNotification.checked=e.data.result.isNotification;
    }
}

const saveUserNotification=async()=>{
    try{
        let user = inputUserNotification.value;
        let request = await fetch("./",{
            method:"POST",
            body:"action=saveUserNotification&user=" + user,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = request.json();
        if(data){
            messg("The notifications user saved sucessfully",true);
        }else{
            messg("The notifications user was not saved",false);
        }
    }catch(error){
        messg("Error unexpected at save the notifications user: "+error,false);
    }
}

function showFormEdit(node){
    containerFormEdit.dataset.id = node.parentNode.parentNode.dataset.id;
    let hostname = node.parentNode.parentNode.querySelector(".info .hostname").textContent;
    containerFormEdit.dataset.hostname = hostname;
    containerFormEdit.querySelector("form > span > span").textContent=node.parentNode.parentNode.querySelector(".info .hostname").textContent;
    containerFormEdit.querySelector("input#hostname").value = hostname;
    containerFormEdit.style.display="block";
}

function showFormAlert(node){
    containerFormNotification.dataset.id = node.parentNode.parentNode.dataset.id;
    containerFormNotification.querySelector("form > span > span").textContent=node.parentNode.parentNode.querySelector(".info .hostname").textContent;
    containerFormNotification.style.display="block";
}

function showUploadBox(node){
    containerUploadFiles.dataset.id = node.parentNode.parentNode.dataset.id;
    containerUploadFiles.dataset.hostname = node.parentNode.parentNode.querySelector(".info .hostname").textContent;
    containerUploadFiles.querySelector("span > span").textContent=node.parentNode.parentNode.querySelector(".info .hostname").textContent;
    containerUploadFiles.style.display="flex";
}

export async function eventsClientsList(e){
    let node = e.target;
    if(node.classList.contains("fa-user-pen")){
        showFormEdit(node);
    }else if(node.classList.contains("fa-power-off")){
        shutdownComputer(node);
    }else if(node.classList.contains("fa-redo")){
        rebootComputer(node);
    }else if(node.classList.contains("fa-moon")){
        suspendComputer(node);
    }else if(node.classList.contains("fa-bell")){
        showFormAlert(node);
    }else if(node.classList.contains("fa-upload")){
        showUploadBox(node);
    }else if(node.classList.contains("fa-camera")){
        screenshot(node);
    }else if(node.classList.contains("fa-ban")){
        listPrograms(node);
    }
}

const checkFormAlert=async(e)=>{
    let node = e.target;
    let type = containerFormNotification.querySelector("select").value;
    let title = containerFormNotification.querySelector("input#title").value;
    let description = containerFormNotification.querySelector("textarea#description").value;
    if(type=="" || title=="" || description == ""){
        messg("There are fields empties",false);
        return false;
    }else if(description.length>120){
        messg("The description is too long",false);
        return false;
    }else if(type!="notification" && type!="error" && type!="info" && type!="warning" && type!="message"){
        messg("This alert type doesn't exist",false);
        return false;
    }
    return await sendAlert(node,type,title,description)
}
// file drag and drop functions
const dragover=(e)=>{
    e.preventDefault();
    containerUploadFiles.classList.add("active");
    containerUploadFiles.querySelector("h2").textContent = "You should drop the file for update it";
}

const dragleave=(e)=>{
    e.preventDefault();
    containerUploadFiles.classList.remove("active");
    containerUploadFiles.querySelector("h2").textContent = "Drag and drop the files here";
}

const drop=(e)=>{
    e.preventDefault();
    let id = e.target.parentNode.dataset.id;
    files = e.dataTransfer.files;
    showFiles(id,files);
    containerUploadFiles.classList.remove("active");
    containerUploadFiles.querySelector("h2").textContent = "Drag and drop the files here";
}

const convertBlob=async(datauri)=>{
    let request = await fetch(datauri);
    let data = await request.blob()
}

const postFile=async(id,file,name,idFile)=>{
    try{
        let request = await fetch(".",{
            method:"POST",
            body: `action=uploadFiles&id=${id}&name=${name}&idFile=${idFile}&file=${file}`,
            headers:{
                "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
                "X-CSRFToken":getCookie("csrftoken")
            }
        });
        let data = await request.json();
        if(data.result){
            document.querySelector(`#${idFile} .status`).innerHTML="<span class='success'>success</span>";
        }
    }catch(error){
        document.querySelector(`#${idFile} .status`).innerHTML="<span class='failure'>failed</span>";
    }
}

const processFile=(id,file)=>{
    const docType = file.type;
    const validExtensions = [
        "image/tiff","image/x-tiff","image/pjpeg","image/x-icon","image/jpg","image/jpeg","image/png","image/gif","image/bmp","image/x-windows-bmp",
        "video/quicktime","video/msvideo","video/x-msvideo","video/avi","video/wmv","video/mov","video/mp4","video/mkv","video/flv","video/mpg","video/mpeg","video/x-mpeg",
        "audio/ogg","audio/wav","audio/x-wav","audio/mpeg3","audio/mpeg","audio/x-mpeg-3",
        "application/pdf",
        "application/msword","application/wordperfect","application/wordperfect6.0",
        "application/vnd.ms-excel","application/excel","application/x-excel","application/x-msexcel","application/excel",
        "application/mspowerpoint","application/powerpoint","application/vnd.ms-powerpoint","application/x-mspowerpoint",
        "application/vnd.oasis.opendocument.text",
        "application/vnd.oasis.opendocument.spreadsheet",
        "application/vnd.oasis.opendocument.presentation",
        "application/vnd.ms-powerpoint",
        "application/vnd.visio",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.ms-excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint","application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "text/plain"
    ];
    if(validExtensions.includes(docType)){
        const fileReader = new FileReader()
        let fileUrl;
        const name = `file-${Math.random().toString(32).substring(7)}`;
        fileReader.addEventListener("load",e=>{
            fileUrl = fileReader.result;
            let url;
            if(docType.toLowerCase().includes("audio")){
                url="/static/images/audio.webp";
            }else if(docType.toLowerCase().includes("video")){
                url="/static/images/video.webp";
            }else if(docType.toLowerCase().includes("pdf")){
                url="/static/images/pdf.webp";
            }else if(docType.toLowerCase().includes("word")){
                url="/static/images/word.webp";
            }else if(docType.toLowerCase().includes("excel")){
                url="/static/images/excel.webp";
            }else if(docType.toLowerCase().includes("powerpoint")){
                url="/static/images/powerpoint.webp";
            }else if(docType.toLowerCase().includes("opendocument") || docType.toLowerCase().includes("officedocument")){
                url="/static/images/libreoffice.webp";
            }else if(docType=="text/plain"){
                url="/static/images/txt.web";
            }else{
                url = fileUrl
            }
            const img = `
                <div id="${name}" class="file-container">
                    <i class="fa fa-circle-xmark delete-file"></i>
                    <img src="${url}" alt="${file.name}">
                    <div>
                        <span>${file.name}</span>
                        <span class="status">uploading...</span>
                    </div>
                </div>
            `;
            containerUploadFiles.querySelector("#preview").innerHTML+=img
            postFile(id,fileUrl,file.name,name);
        });
        fileReader.readAsDataURL(file);
    }else{
        messg("The file type is not valid",false);
    }
}

const showFiles=(id,files)=>{
    if(files.length == undefined){
        processFile(files);
    }else{
        for(const file of files){
            processFile(id,file);
        }
    }
}

const uploadFile=(e)=>{
    containerUploadFiles.classList.add("active");
    let id = containerUploadFiles.dataset.id;
    files = containerUploadFiles.querySelector("div:first-child input#uploadFile").files;
    showFiles(id,files);
    containerUploadFiles.classList.remove("active");
}

const deleteFile=async(id,filename)=>{
    let request = await fetch("./",{
        method:"POST",
        body:`action=deleteFile&id=${id}&filename=${filename}`,
        headers:{
            "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
            "X-CSRFToken":getCookie("csrftoken")
        }
    });
    let data = request.json();
}

const filterPrograms=(e)=>{
    let search = e.target.value;
    printListPrograms(search)
}
const fetchProgramsDeny=async(id,list)=>{
    let request = await fetch("./",{
        method:"POST",
        body:`action=denyPrograms&id=${id}&list=${list}`,
        headers:{
            "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
            "X-CSRFToken":getCookie("csrftoken")
        }
    });
    let data = await request.json();
    if(data.result){
        messg("The programs selected has denied in the client computer successfully",true);
    }else{
        messg("Error unexpected at deny the programs in the client computer",false)
    }
}

const denyPrograms=async(e)=>{
    let programs = containerListPrograms.querySelectorAll("div > label input[type='checkbox']:checked");
    let listPrograms=[];
    programs.forEach(program=>{
        listPrograms.push(program.id)
    });
    let data = (listPrograms.length==0)?null:listPrograms;
    await fetchProgramsDeny(e.target.parentNode.dataset.id,data);
}

export async function pageDashboard(){
    // animation open configuration
        buttonConf.addEventListener("click",()=>config.style.right="0");

    // animation close configuration
        closeConf.addEventListener("click",()=>config.removeAttribute("style"));
        enterSession();

    // This checks if the session cookie is expired.
        await cookie();

        saveConf.addEventListener("click",await saveConfig);
        newOTP.addEventListener("click",await reloadOTP);
        buttonLogout.addEventListener("click", sessionLogout);

    // updates in real time
        showAliveServer();
        updateListClients();
        showAliveData();

    // enable / disable notification checkbox
        checkboxNotification.checked=checkNotification;
        checkboxNotification.addEventListener("click",await activeDisableNotifications);
        buttonUserNotification.addEventListener("click",await saveUserNotification);

    // list clients' events (notification,edit hostname,shutdown,...)
        containerClients.addEventListener("click",await eventsClientsList);

    // edit client hostnamename
        containerFormEdit.querySelector(".fa-circle-xmark").addEventListener("click",()=>containerFormEdit.removeAttribute("style"));
        containerFormEdit.querySelector("#buttonEditClient").addEventListener("click",await editHostName);

    // send alert at client
        containerFormNotification.querySelector(".fa-circle-xmark").addEventListener("click",()=>containerFormNotification.removeAttribute("style"));
        containerFormNotification.querySelector("#buttonSendAlert").addEventListener("click",await checkFormAlert);

    // events for drag and drop files
        closeUploadFiles.addEventListener("click",()=>{
            inputUploadFiles.value="";
            containerUploadFiles.querySelector("#preview").innerHTML="";
            containerUploadFiles.removeAttribute("style");
        });
        containerUploadFiles.addEventListener("click",async(e)=>{
            let node = e.target;
            if(node.classList.contains("delete-file")){
                let filename = node.parentNode.querySelector("img").alt;
                let id = node.parentNode.parentNode.parentNode.dataset.id;
                await deleteFile(id,filename);
                node.parentNode.remove();
            }else if(!node.classList.contains("fa-circle-xmark")){
                inputUploadFiles.click()
            }
        });
        containerUploadFiles.addEventListener("change",uploadFile);
        containerUploadFiles.addEventListener("dragover",dragover);
        containerUploadFiles.addEventListener("dragleave",dragleave);
        containerUploadFiles.addEventListener("drop",drop);
        containerUploadFiles.querySelector("span#extensions").addEventListener("click",()=>e.preventDefault());

    // event for list programs to deny
        containerListPrograms.querySelector("i.fa-circle-xmark").addEventListener("click",()=>containerListPrograms.removeAttribute("style"));
        containerListPrograms.querySelector("input[type='search']").addEventListener("keyup",filterPrograms);
        containerListPrograms.querySelector("input[type='button']").addEventListener("click",await denyPrograms);
}