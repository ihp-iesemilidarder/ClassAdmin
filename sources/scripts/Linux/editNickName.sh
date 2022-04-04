#!/bin/bash
currentUser=$1
newUser=$2

if [[ -z $* ]];then
        echo -e "\033[1;31m[!]\033[0m The scripts needs two params.\n\teditNickName.sh <nickNameCurrent> <newNickNmae>"
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

operation "replacing the user $currentUser by $newUser." $(sed -i "s/$currentUser/$newUser/g" /lib/systemd/system/ClassAdmin.service)
sleep 1
operation "restarting systemctl daemons." "systemctl daemon-reload"
sleep 1
operation "restarting ClassAdmin service." "systemctl restart ClassAdmin"
