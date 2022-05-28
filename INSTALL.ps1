# Author: Ivan Heredia Planas
# 2 CFGS ASIX
#
# This script file is used for install the service client in Windows
#
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
[Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Insufficient permissions to run this script."
    Break
}

function deleteClassAdminSData(){
    Write-Host "=========================================================================================="
    Write-Host "Deleting ClassAdmin Server data"
    Write-Host "=========================================================================================="
    Remove-Item -Path "./Django" -Recurse -Force 2> $nul;
    Remove-Item -Path "./init.sql" -Recurse -Force;
    Remove-Item -Path "./services/ClassAdminS.socket" -Recurse -Force;
    Remove-Item -Path "./Daemon/ClassAdminS.service" -Recurse -Force;
    Write-Host "[success]" -ForegroundColor Green;
}

function librariesPython3(){
    Write-Host "=========================================================================================="
    Write-Host "Installing python3 libraries."
    Write-Host "=========================================================================================="
    py -m pip install json 2> $null;
    py -m pip install otp 2> $null;
    py -m pip install hashlib 2> $null;
    py -m pip install base64 2> $null;
    py -m pip install requests 2> $null;
    py -m pip install io 2> $null;
    py -m pip install random 2> $null;
    py -m pip install wheel 2> $null;
    py -m pip install utils 2> $null;
    py -m pip install mysql.connector 2> $null;
    py -m pip install binascii 2> $null;
    py -m pip install math 2> $null;
    py -m pip install os 2> $null;
    py -m pip install sys 2> $null;
    py -m pip install platform 2> $null;
    py -m pip install Image 2> $null;
    py -m pip install mariadb 2> $null;
    py -m pip install sockets 2> $null;
    py -m pip install threading 2> $null;
    py -m pip install multiprocessing 2> $null;
    py -m pip install pywin32 2> $null;
    py -m pip install psutil 2> $null;
    py -m pip install pymysql 2> $null;
    py -m pip install pysmb 2> $null;
    py -m pip install pyscreenshot 2> $null;
    Write-Host "[success]" -ForegroundColor Green;
}

function addSystemEnvironmentVariables(){
    Write-Host "=========================================================================================="
    Write-Host "Adding system enviroment variables."
    Write-Host "=========================================================================================="
    New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment' -Name "CLASSADMIN_HOME" -PropertyType "String" -Value "C:\Program Files\ClassAdmin";
    New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment' -Name "CLASSADMIN_LOG" -PropertyType "String" -Value "C:\Program Files\ClassAdmin\ClassAdmin.log";
    New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment' -Name "CLASSADMIN_SSL" -PropertyType "String" -Value "C:\Program Files\ClassAdmin\ssl";
    New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment' -Name "PYTHONPATH" -PropertyType "String" -Value "C:\Program Files\ClassAdmin";
    $valuePath = (Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "Path").Path
    if((Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "Path").Path.indexOf("C:\Program Files\nssm-2.24\win64") -eq -1){
        $valuePath+=";C:\Program Files\nssm-2.24\win64";
        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "path" -Value $valuePath 2> $null;
    }
    if((Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "Path").Path.indexOf("C:\Program Files\ClassAdmin\commands\Windows") -eq -1){
        $valuePath+=";C:\Program Files\ClassAdmin\commands\Windows";
        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "path" -Value $valuePath 2> $null;
    }
    Write-Host "[success]" -ForegroundColor Green;
}

function ask($question,$info){
    Write-host "=========================================================================================="
    do{
        Write-Host $info;
        Write-Host "[i]" -ForegroundColor Blue -NoNewline;
        $ask=Read-Host "$question [Y/n]";
    }while($ask -ne "Y");
}

function installCABundle(){
    Write-Host "=========================================================================================="
    Write-Host "Installing ClassAdmin CA Bundle."
    Write-Host "=========================================================================================="
    Import-Certificate -FilePath .\ssl\ClassAdmin.crt -CertStoreLocation "Cert:\LocalMachine\Root";
    Write-Host "[success]" -ForegroundColor Green;
}

function addHosts(){
    Write-Host "=========================================================================================="
    Write-Host "Editing hosts file"
    Write-Host "=========================================================================================="
    Write-Host "[?]" -ForegroundColor Blue -NoNewline
    $server = Read-Host " Which is ClassAdminS server IP address?";
    Add-Content 'C:\Windows\system32\drivers\etc\hosts' "$server    classadmin.server"
    Write-Host "Domain classadmin.server added to hosts file" -NoNewline;
    Write-Host "[success]" -ForegroundColor Green;
}

function installService($service,$description){
    Write-Host "=========================================================================================="
    Write-Host "Installing $service service."
    Write-Host "=========================================================================================="
    $user = $env:USERNAME;
    nssm remove ClassAdmin confirm;
    nssm install $service "C:\Users\$user\AppData\Local\Programs\Python\Python310\python.exe" "$service.socket";
    nssm set $service AppDirectory 'C:\Program Files\ClassAdmin\services';
    nssm set $service DisplayName $service;
    nssm set $service Description "$description";
    nssm set $service Start SERVICE_AUTO_START;
    nssm set $service DependOnService Schedule;
    nssm set $service AppPriority BELOW_NORMAL_PRIORITY_CLASS;
    nssm set $service ObjectName "$user";
    Write-Host "[i]" -ForegroundColor Blue -NoNewline;
    Write-Host " You go to 'Log On' and you type the username and password of local machine.You indicates the username '.\$user'. This indicates the user that will run the service."
    nssm edit $service;
    Write-Host "[success]" -ForegroundColor Green;
}

function activeNotifications(){
    Write-Host "[?]" -ForegroundColor Blue -NoNewline;
    $notificationAsk = Read-Host "Do you want that ClassAdmin service send system notifications? [true/false]";
    if($notificationAsk -eq "true" -or $notificationAsk -eq "false"){
        $result = '"notifications":"'+$notificationAsk+'",';
        (Get-Content './services/ClassAdmin.conf') | %{$_ -replace '"notifications"(.*)',$result} | Set-Content '.\services\ClassAdmin.conf';
        Write-Host "[success]" -ForegroundColor Green;
    }
}

function createClassAdminUser(){
    Write-Host "=========================================================================================="
    Write-Host "Creating ClassAdmin user."
    Write-Host "=========================================================================================="
    New-LocalUser -Description "ClassAdmin" -Name "ClassAdmin" -FullName "ClassAdmin" -PasswordNeverExpires -AccountNeverExpires -UserMayNotChangePassword -Confirm:$false -Password ("12345678" | ConvertTo-SecureString -AsPlainText -Force);
    Write-Host "[success]" -ForegroundColor Green;
}

Write-Host "[?]" -ForegroundColor Blue -NoNewline;
$ask=Read-Host " Do you want install the ClassAdminS server or ClassAdmin client? [ClassAdmin/ClassAdminS]";

if($ask -eq "ClassAdmin"){
    Write-Host "I need your help, for I can install you the ClassAdmin. So I will need you do some installations by me. Please.";
    ask "I need install the Python3 with version granter or equal than 3.8. Do you have installed it?" "official web: https://www.python.org/downloads/. During the installation you check 'Add python 3.x to PATH' at start and the end you click in 'Disable path length limit'";
    ask "I need install NSSM. Do you have installed it?" "official web: nssm.cc. Extract it in C:\Program Files";
    ask "I need install Microsoft C++ Build Tools, and install the 'Visual C++ build tools' (Desarrollo para escritorio con C++). Do you have installed it?" "official web: http://visualstudio.microsoft.com/visual-cpp-build-tools/"
    deleteClassAdminSData;
    librariesPython3;
    addSystemEnvironmentVariables;
    installCABundle;
    addHosts;
    installService $ask "Start ClassAdmin Client";
    activeNotifications;
    createClassAdminUser;
    Write-Host "[!]" -ForegroundColor Blue -NoNewline;
    Write-Host " start CMD as administrator and you execute: nssm start ClassAdmin."
}elseif($ask -eq "ClassAdminS"){
}else{
    Break;
}