#!/bin/bash
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
# This script edits the local machine hostname
#
newHostName=$1

if [[ -z $* ]];then
        echo -e "\033[1;31m[!]\033[0m The scripts needs two params.\n\teditHostName.sh <newHostName>"
        exit
fi

function loading(){
        while [ true ]
        do
                echo -ne "."
                sleep 2
        done
}

function operation(){
        echo -ne $1
        loading&
        PID_loading=$!
        # if the installation or uninstallation have dialogs, it doesn't show it, but is executed.
        if [[ $3 = 1 ]];then
                $2
                echo -ne "\033[1;32mOK\033[0m"
        else
                $2
                #DEBIAN_FRONTEND=nointeractive $2 > /dev/null 2>&1
                echo -ne "\033[1;32mOK\033[0m"
        fi
        kill -19 $PID_loading > /dev/null 2>&1
        echo ""
}

operation "changing the hostname $(hostname) by $newHostName." $(hostnamectl set-hostname $newHostName)
sleep 1
operation "restarting computer." "systemctl restart ClassAdmin"