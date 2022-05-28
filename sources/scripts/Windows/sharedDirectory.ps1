# Author: Ivan Heredia Planas
# ivanherediaplanas@protonmail.com
#
# Licensed by GNU GENERAL PUBLIC LICENSE VERSION 3
# This file is part of ClassAdmin.
# ClassAdmin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# ClassAdmin is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with ClassAdmin. If not, see <https://www.gnu.org/licenses/>.
# Copyright 2022 Ivan Heredia Planas
#
# This script copy a file to a shared folder. Used for the functionally of screenshots
#

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