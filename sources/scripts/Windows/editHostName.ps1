Param(
    [String] $newHostname
)
if(!$newNickName){
    Write-Host '[!]' -ForegroundColor Red -NoNewline
    Write-Host ' The script needs one argument.'
    Write-Host '    editNickName.ps1 -newNickName <name>'
    exit
}
Write-Host "Replacing the user $currentHostname by $newNickName " -NoNewline
nssm set ClassAdmin AppParameters "ClassAdmin.socket $newNickName"
Write-Host "OK" -ForegroundColor Green
timeout 3
Write-Host "Stopping ClassAdmin service. " -NoNewline
restart-service ClassAdmin
Write-Host "OK" -ForegroundColor Green