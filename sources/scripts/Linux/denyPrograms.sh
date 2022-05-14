#!/bin/bash
#
# This script deby the binaries passed by arguments.
#

function allowPrograms(){
	while IFS= read -r line;
	do
		if [[ $line != "" ]];then
			chmod a+x $line
		fi
	done < /etc/ClassAdmin/sources/scripts/Linux/denyPrograms.deny
	echo "" > /etc/ClassAdmin/sources/scripts/Linux/denyPrograms.deny
}

function denyPrograms(){
	for program in $@
	do
		local path
		path=$(command -v -- "$program")
		path=$(readlink -e -- "$path")
		echo $path >> /etc/ClassAdmin/sources/scripts/Linux/denyPrograms.deny
		chmod a-x $path
	done
	chmod 600 /etc/ClassAdmin/sources/scripts/Linux/denyPrograms.deny
}

function init(){
	if [[ -e /etc/ClassAdmin/sources/scripts/Linux/denyPrograms.deny ]];then
		allowPrograms
	fi
	denyPrograms $@
}

init $@