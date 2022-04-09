Param(
    [String] $newHostname
)
if(!$newHostName){
    Write-Host '[!]' -ForegroundColor Red -NoNewline
    Write-Host ' The script needs one argument.'
    Write-Host '    editHostName.ps1 -newHostName <name>'
    exit
}
Write-Host "Changing the hostname by $newHostname " -NoNewline
Rename-Computer -ComputerName $env:COMPUTERNAME -NewName $newHostname -Restart