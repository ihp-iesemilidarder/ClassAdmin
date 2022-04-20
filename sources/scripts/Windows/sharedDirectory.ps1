Param(
    [String] $Operation,
    [String] $Server,
    [String] $Username,
    [String] $Password,
    [String] $SharedDirectory,
    [String] $FileName,
    [String] $File
)
if(!$Operation -or !$Server -or !$Username -or !$Password -or !$SharedDirectory -or !$FileName -or !$File){
    Write-Host '[!]' -ForegroundColor Red -NoNewline
    Write-Host ' The script needs six arguments.'
    Write-Host '    screenshot.ps1 -Operation <add|delete> -Server <ip> -Username <username> -Password <password> -SharedDirectory <path> -FileName <filename> -File <path_to_file|file__to_remove>'
    exit
}
net use \\$server\$SharedDirectory /USER:$Username $Password
if($Operation -eq "Add"){
    Copy-Item -Path $File -Destination \\$server\$SharedDirectory\$FileName
}elseif($Operation -eq "Delete"){
        Remove-Item \\$server\$SharedDirectory\$File
}