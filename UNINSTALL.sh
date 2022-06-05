#!/bin/bash
# Author: Ivan Heredia Planas
# 2 CFGS ASIX
#
# This script file is used for uninstall the service (server or client) in Linux
#

if [[ $(whoami) != "root" ]];then
	echo -e "\033[1;31m[-]\033[0m You aren't root"
	exit
fi

function operation(){
	function loading(){
		while [ true ]
		do
			echo -ne "."
			sleep 2
		done
	}
	echo -ne $1
	loading&
	PID_loading=$!
	# if the installation or uninstallation have dialogs, it doesn't show it, but is executed.
	if [[ $3 = 1 ]];then
		$2
		echo -ne "\033[1;32mOK\033[0m"
	else
		DEBIAN_FRONTEND=nointeractive $2 > /dev/null 2>&1
		echo -ne "\033[1;32mOK\033[0m"
	fi
	kill -19 $PID_loading > /dev/null 2>&1
	echo ""
}
if [[ $@ == "-F" ]];then
	:
else
	echo -ne "Do you want uninstall ClassAdmin services? [Y/n] "
	read ask
	if [[ $ask == "Y" ]] || [[ $ask == "y" ]];then
		:
	else
		exit 1
	fi
fi
operation "Stopping services." $(systemctl stop ClassAdmin 2> /dev/null; systemctl stop ClassAdminS 2> /dev/null)
operation "Deleting environment variables." $(sed -i '/CLASSADMIN/d' /etc/environment 2> /dev/null; sed -i "/PYTHONPATH/d" /etc/environment 2> /dev/null)
operation "Deleting ClassAdmin CA Bundle." $(sed -uz -n 10 /usr/local/share/ca-certificates/ClassAdmin* 2> /dev/null; update-ca-certificates 2> /dev/null)
operation "Deleting apache2 environment variables created by ClassAdmin software." $(sed -i '/CLASSADMIN/d' /etc/apache2/envvars 2> /dev/null)
operation "Changing the permissions alterated by ClassAdmin software." $(chown o-w /var/log 2> /dev/null)
operation "Changing the Mysql/MariaDB configuration alterated by ClassAdmin software." $(sed -i 's/0.0.0.0/127.0.0.1/g' /etc/mysql/mariadb.conf.d/50-server.cnf 2> /dev/null; sed -i 's/0.0.0.0/127.0.0.1/g' /etc/mysql/mysql.conf.d/mysqld.cnf 2> /dev/null)
operation "Deleting ClassAdmin database." $(mysql -u root -p12345678 -e 'DROP DATABASE ClassAdmin;' 2> /dev/null)
operation "Deleting apache2 ClassAdminS VirtualHosts." $(a2dissite ClassAdmin* 2> /dev/null; shred -uz -n 10 /etc/apache2/sites-available/ClassAdmin* 2> /dev/null)
operation "Deleting user ClassAdmin in mySQL." $(mysql -u root -p12345678 -e 'DROP USER ClassAdmin;' 2> /dev/null)
operation "Deleting ClassAdmin hosts." $(sed -i '/classadmin.server/d' /etc/hosts 2> /dev/null)
operation "Deleting ClassAdmin user." $(deluser --remove-all-files ClassAdmin 2> /dev/null)
# With the help of Dudi Boy (stackoverflow)
# https://stackoverflow.com/questions/72324373/how-to-select-a-group-lines-by-your-content-of-a-file-in-gnu-linux
operation "Deleting X Server permissions added for ClassAdmin software." $(sed -i "$(cat -n /etc/profile | gawk '/if \[ "\$DISPLAY" != "" \]/,/fi/{print $1}' | tr '\n' ',' | sed 's/,$//g' | sed -E 's/,(.+),/,/g')d" /etc/profile)
operation "Deleting shared folder of ClassAdmin software." $(sed "$(cat -n /etc/samba/smb.conf | gawk '/\[ClassAdminS_Screenshots\]/,/force group = www-data/{print $1}' | tr '\n' ',' | sed 's/,$//g' | sed -E 's/,(.+),/,/g')d" /etc/samba/smb.conf)
operation "Deleting the ClassAdmin data." $(find / -iname '*ClassAdmin*' -exec rm -rf {} + 2> /dev/null)
operation "Restarting Linux services." $(systemctl daemon-reload 2> /dev/null)
echo -e "\033[1;32m[+]\033[0m Uninstallation completed"
