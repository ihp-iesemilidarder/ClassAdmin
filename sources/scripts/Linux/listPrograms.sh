#!/bin/bash
#
# This script list the programs of client computer
#

function getListPrograms(){
	listPrograms=`ls /usr/share/applications/*.desktop`
	listPrograms=(${listPrograms// /})
}

# helped by Stéphane Chazelas (Unix & Linux)
# https://unix.stackexchange.com/questions/702494/how-to-pass-a-parameter-in-a-command-without-run-the-parameter-content/702495#702495
function denyCheck(){
	local file
	file=$(command -v -- "$1")
	file=$(readlink -e -- "$file") && [ -x "$file" ] && REPLY=$file
} 2> /dev/null

function getJSON(){
	for index in ${!listPrograms[@]}
	do
		last=$((${#listPrograms[@]}-1))
		name=`cat ${listPrograms[$index]} | grep -E "^Name="`
		IFS="=" read -ra name <<< $name
		name=${name[1]}
		binary=`cat "${listPrograms[$index]}" | grep -E "^Exec="`
		IFS="=" read -ra binary <<< "$binary"
		binary="${binary[1]}"
		IFS=" " read -ra binary <<< "$binary"
		if denyCheck "${binary/%$'\r'/}";then
			deny="false"
		else
			deny="true"
		fi
		if [[ $last = $index ]];then
			json=$json"\"${name/%$'\r'/}\":[\"${binary/%$'\r'/}\",$deny]}" # delete the ^M of string
		elif [[ $index = 0 ]];then
			json=$json"{\"${name/%$'\r'/}\":[\"${binary/%$'\r'/}\",$deny],"
		else
			json=$json"\"${name/%$'\r'/}\":[\"${binary/%$'\r'/}\",$deny],"
		fi
	done
}

function saveListPrograms(){
	echo $json > /tmp/listPrograms.txt
	smbclient //$1/$2 $4 -U $3 -c "put /tmp/listPrograms.txt listPrograms.txt"
	shred -uz -n 5 /tmp/listPrograms.txt
}

function init(){
	getListPrograms
	json=""
	getJSON
	saveListPrograms $1 $2 $3 $4
	shred -uz -n 3 /tmp/listPrograms.txt
}
if [[ -z $#  || $# != 5 ]];then
	echo -e "\033[1;31m[-]\033[0m The scripts needs four arguments"
	echo -e "\tlistprograms.sh <server> <sharedDirectory> <username> <password>"
	exit
fi
init $1 $2 $3 $4