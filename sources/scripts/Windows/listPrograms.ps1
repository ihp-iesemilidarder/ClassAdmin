#
# This script generates a system program list installed. Used for the functionally of deny programs.
#

Param(
    [String] $SharedDestination,
    [String] $Username,
    [String] $Password
)
if(!$SharedDestination -or !$Username -or !$Password){
    Write-Host '[!]' -ForegroundColor Red -NoNewline;
    Write-Host ' The script needs three arguments.';
    Write-Host '    listPrograms.ps1 -SharedDestination <path_in_network> -Username <username> -Password <password>';
    exit;
}
function addExe($1,$el, $list){
    $splitName = $1.CreateShortcut($el.FullName).FullName.Split("\");
    $name = $splitName[$splitName.Length-1];
    $name = $name.Substring(0,$name.Length-4);
    $splitPath = $1.CreateShortcut($el.FullName).TargetPath.Split("\");
    $path = $splitPath[$splitPath.Length-1];
    if(!$Global:exes.ContainsValue($path)){
        $Global:exes.Add($name,$path);
    }
}

function showPrograms($1){
    $lnks = Get-ChildItem -Path $1 -Recurse -Filter "*.lnk";
    $sh = New-Object -ComObject WScript.Shell;
    $lnks | ? {$sh.CreateShortcut($_.FullName).TargetPath -match "exe$"} | ForEach-Object {addExe $sh $_ $exes};
    foreach($exe in $exes){
        if(!$Global:programs.Contains($exe) -or $name -icontains "install" -or $name -icontains "setup"){
            $Global:programs.Add($exe);
        }
    }
}

function init(){
    [collections.arraylist]$Global:programs = @();
    $Global:exes = @{};
    showPrograms "C:\ProgramData\Microsoft\Windows\Start Menu\Programs";
    showPrograms "C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs";
    echo $Global:programs.ToString().Length;
    $Global:exes | ConvertTo-Json | Out-File 'C:\Program Files\ClassAdmin\transfers\listPrograms.txt';
    net use $sharedDestination /USER:$Username $Password;
    Copy-Item -Path 'C:\Program Files\ClassAdmin\transfers\listPrograms.txt' -Destination $sharedDestination;
    Remove-Item -Path 'C:\Program Files\ClassAdmin\transfers\listPrograms.txt';
}
init;