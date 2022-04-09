Param(
    [String] $newHostname
)
if(!$newHostName){
    Write-Host '[!]' -ForegroundColor Red -NoNewline
    Write-Host ' The script needs one argument.'
    Write-Host '    editHostName.ps1 -newHostName <name>'
    exit
}
Write-Host "Replacing the user $currentHostname by $newHostName " -NoNewline
nssm set ClassAdmin AppParameters "ClassAdmin.socket $newHostName"
Write-Host "OK" -ForegroundColor Green
timeout 3
Write-Host "Stopping ClassAdmin service. " -NoNewline
restart-service ClassAdmin
Write-Host "OK" -ForegroundColor Green