Param(
    [Switch] $Force
)
if(!$Force){
    $permission = Read-Host -Prompt "Do you want uninstall ClassAdmin proyect? [Y/n]";
    if($permission -ne "Y" -or $permission -ne "y"){
        Write-Host "[-]" -ForegroundColor Red -NoNewline;
        Write-Host " Good Bye";
        exit;
    }
}

function deleteEnvironmentsVariables(){
    Write-Host "Deleting system environment variables added by ClassAdmin proyect." -NoNewline;
    Remove-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "CLASSADMIN_HOME" 2> $null;
    Remove-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "MOD_WSGI_APACHE_ROOTDIR" 2> $null;
    Remove-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "CLASSADMIN_LOG" 2> $null;
    Remove-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "CLASSADMIN_SSL" 2> $null;
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "PYTHONPATH" -Value "" 2> $null;
    $valuePath = (Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "Path").Path.replace("C:\Program Files\ClassAdmin\commands\Windows;","") 2> $null;
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" -Name "path" -Value $valuePath 2> $null;
    Write-Host "OK" -ForegroundColor Green;
}

function deleteConfigurationXampp(){
    Write-Host "Changing xampp configuration alterated by ClassAdmin proyect." -NoNewline;
    (Get-Content 'C:\xampp\apache\conf\httpd.conf' 2> $null) | %{$_ -replace 'Include "conf/extra/django.conf"',''} 2> $null | Set-Content 'C:\xampp\apache\conf\httpd.conf' 2> $null;
    Remove-Item 'C:\xampp\apache\conf\extra\ClassAdminS.conf' 2> $null;
    Write-Host "OK" -ForegroundColor Green;
}

function deleteScheduleTask(){
    Write-Host "Deleting schedule task created for ClassAdmin." -NoNewline;
    Stop-ScheduledTask -TaskName django 2> $null;
    Unregister-ScheduledTask -TaskName django 2> $null;
    Write-Host "OK" -ForegroundColor Green;
}

function deleteHosts(){
    Write-Host "Changing hosts alterated for ClassAdmin." -NoNewline;
    (Get-Content 'C:\Windows\system32\drivers\etc\hosts' 2> $null) | %{$_ -replace '(.*)classadmin.server(.*)',''} 2> $null | Set-Content 'C:\Windows\system32\drivers\etc\hosts' 2> $null;
    Write-Host "OK" -ForegroundColor Green;
}

function deleteSSLXampp(){
    Write-Host "Changing XAMPP Apache SSL configuration alterated for ClassAdmin." -NoNewline;
    (Get-Content 'C:\xampp\apache\conf\extra\httpd-ssl.conf' 2> $nul) | %{$_ -replace '(.*)"C:\\Program Files\\ClassAdmin\\ssl\\ClassAdmin.(.*)"',''} 2> $null | Set-Content 'C:\xampp\apache\conf\extra\httpd-ssl.conf' 2> $null;
    Write-Host "OK" -ForegroundColor Green;
}

function deleteClassAdminService(){
    Write-Host "Disabling ClassAdmin." -NoNewline;
    nssm stop ClassAdmin 2> $null;
    nssm stop ClassAdminS 2> $null;
    nssm remove ClassAdmin confirm 2> $null;
    nssm remove ClassAdminS confirm 2> $null;
    Write-Host "OK" -ForegroundColor Green;
}

function deleteClassAdminUser(){
    Write-Host "Deleting ClassAdmin local user." -NoNewline;
    Remove-LocalUser -Name "ClassAdmin" 2> $null;
    Write-Host "OK" -ForegroundColor Green;
}

function deleteSMBShare(){
    Write-Host "Deleting ClassAdmin SMB Share" -NoNewline;
    Remove-SmbShare -Name "ClassAdminS_Screenshots" 2> $null;
    Write-Host "OK" -ForegroundColor Green;
}

function init(){
    deleteEnvironmentsVariables;
    deleteConfigurationXampp;
    deleteScheduleTask;
    deleteHosts;
    deleteSSLXampp;
    deleteClassAdminService;
    deleteClassAdminUser;
    deleteSMBShare;
}
init;