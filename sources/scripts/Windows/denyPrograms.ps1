#
# This script deny the programs specified
#

Param(
    [String] $Programs
)

if(!$Programs){
    Write-Host '[!]' -ForegroundColor Red -NoNewline;
    Write-Host ' The script needs one argument.';
    Write-Host '    denyPrograms.ps1 -Programs "<exe1>,<exe2>,<exe3>[,...]" ';
    exit;
}

function prepareForDeny($path){
    Get-Item -Path "$path" 2> $nul;
    try{
        New-Item -Path "$path\SOFTWARE\Microsoft\Windows\CurrentVersion" -Name "Policies";
    }catch{
        $null;
    }
    try{
        New-Item -Path "$path\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies" -Name "explorer";
    }catch{
        $null;
    }
    try{
        New-ItemProperty -Path "$path\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\explorer" -PropertyType DWord -Value 1 -Name "DisallowRun";
    }catch{
        $null;
    }
    try{
        New-Item -Path "$path\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\explorer" -Name "DisallowRun";
    }catch{
        $null;
    }
}

function denyPrograms($path){
    Clear-Item -Path "$path\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\explorer\DisallowRun";
    foreach($program in $Global:listPrograms){
        New-ItemProperty -Path "$path\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\explorer\DisallowRun" -PropertyType String -Name $program -Value $program;
    }
}

function currentUsers(){
    $Global:currentUsers = Get-Item -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\S-1-5-21*" | ForEach-Object {$_.Name.Split("\")[$_.Name.Split("\").Length-1]};
    foreach($ssid in $Global:currentUsers){
        $root = "HKU:\$ssid";
        if(Get-Item -Path "$root" 2> $nul){
            prepareForDeny $root;
            $Global:listPrograms=$Programs -split ",";
            denyPrograms $root;
        }
    }
}
function init(){
    New-PSDrive HKU Registry HKEY_USERS > $null;
    currentUsers;
}

init;