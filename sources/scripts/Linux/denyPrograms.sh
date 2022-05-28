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