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
# This script install the ClassAdmin software.
#
if [[ $(whoami) != "root" ]];then
        echo -e "\033[1;31m[-]\033[0m You aren't root"
        exit
fi

# If you want to look the process. Uncomment this function and comment the current operation function
#
#function operation(){
#  echo "================================================================================================================"
#  echo $1
#  echo "================================================================================================================"
#  $2
#}
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
echo -ne "Do you want install the ClassAdminS server or ClassAdmin client? [ClassAdmin/ClassAdminS]: "
read ask
if [[ $ask == "ClassAdmin" ]];then
        operation "Updating repositories." "apt-get update -y"
        operation "Installing packages." "apt-get install -y python3 python3-pip git zenity scrot pm-utils smbclient"
        operation "Deleting ClassAdminS server data" "rm -rf ./Django && rm -f ./init.sql && rm -f ./services/ClassAdminS.socket && rm -f ./Daemon/ClassAdminS.service"
        operation "Installing python3 libraries." $(pip3 install json 2> /dev/null; pip3 install hashlib 2> /dev/null; pip3 install base64 2> /dev/null; pip3 install requests 2> /dev/null; pip3 install io 2> /dev/null; pip3 install random 2> /dev/null; pip3 install binascii 2> /dev/null; pip3 install math 2> /dev/null; pip3 install os 2> /dev/null; pip3 install sys 2> /dev/null; pip3 install platform 2> /dev/null; pip3 install psutil 2> /dev/null; pip3 install mysql.connector 2> /dev/null; pip3 install pymysql 2> /dev/null; pip3 install pyscreenshot 2> /dev/null; pip3 install pysmb 2> /dev/null; pip3 install socket 2> /dev/null; pip3 install multiprocessing 2> /dev/null; pip3 install threading 2> /dev/null; pip3 install ssl 2> /dev/null; pip3 install time 2> /dev/null; pip3 install urllib3 2> /dev/null; pip3 install re 2> /dev/null; pip3 install datetime 2> /dev/null; pip3 install signal 2> /dev/null; pip3 install logging 2> /dev/null; pip3 install certifi 2> /dev/null)
        operation "Adding environtment variables." $(sed -i '/CLASSADMIN/d' /etc/environment && echo 'CLASSADMIN_HOME=/etc/ClassAdmin' >> /etc/environment && echo 'CLASSADMIN_LOG=/var/log/ClassAdmin.log' >> /etc/environment && echo 'CLASSADMIN_SSL=/etc/ClassAdmin/ssl' >> /etc/environment && sed -i '/PYTHONPATH/d' /etc/environment && echo 'PYTHONPATH=/etc/ClassAdmin' >> /etc/environment)
        operation "Installing ClassAdmin CA Bundle." $(cp ./ssl/ClassAdmin.crt /usr/local/share/ca-certificates && update-ca-certificates)
        server=""
        while [[ $(echo $server | grep -E -o "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}") == "" ]];
        do
        	echo -ne "\033[1;34m[?]\033[0m Which is ClassAdminS server IP address?: "
        	read server
        done
        operation "Adding dns in /etc/hosts." $(sed -i '/classadmin.server/d' /etc/hosts && echo "$server     classadmin.server" >> /etc/hosts)
        operation "Installing ClasAdmin service." $(cp ./Daemon/ClassAdmin.service /lib/systemd/system && systemctl daemon-reload)
	      notification=""
        while [[ $notification != "true" && $notification != "false" ]];
        do
        	echo -ne "\033[1;34m[?]\033[0m Do you want that ClassAdmin service send system notifications? [true/false]: "
        	read notification
        done
        operation "Configurating notifications." $(sed -E -i "s/\"notifications\": \"(.*)\"/\"notifications\": \"$notification\"/g" ./services/ClassAdmin.conf)
        user=""
        while [[ $user == "" ]];
        do
        	echo -ne "The notifications will be execute as user...: "
        	read user
        done
        operation "Notifications will be execute as $user." $(sed -i -E "s/\"user\":(.*)/\"user\":\"$user\"/g" ./services/ClassAdmin.conf)
        operation "Changing permissions for ClassAdmin proyect." $(chmod o+w /var/log 2> /dev/null && chown -R root:www-data . 2> /dev/null && chmod -R g+w . 2> /dev/null && chown www-data:ClassAdmin ./transfers/.screenshots/ 2> /dev/null && chmod -R 770 ./transfers/.screenshots 2> /dev/null && chown www-data:www-data /var/log/ClassAdmin.log)
        operation "Creating ClassAdmin user." $(useradd -p $(openssl passwd -6 12345678) -d /home/ClassAdmin -m -k --badname ClassAdmin)
        operation "Grantting permissons to X Server." $(echo 'if [ "$DISPLAY" != "" ]' >> /etc/profile && echo 'then' >> /etc/profile && echo "	xhost +si:localuser:root" >> /etc/profile && echo 'fi' >> /etc/profile && xhost +si:localuser:root)
        operation "Enabling ClassAdmin service in the boot." $(systemctl enable ClassAdmin)
        operation "Starting ClassAdmin service." $(systemctl start ClassAdmin)
	      echo -e "\033[1;32m[+]\033[0m ClassAdmin installation completed"
elif [[ $ask == "ClassAdminS" ]];then
        operation "Updating repositories." "apt-get update -y"
        operation "Deleting ClassAdmin client data." "rm -f ./services/ClassAdmin.socket && rm -f ./Daemon/ClassAdmin.service"
        operation "Installing packages." "apt-get install -y apache2 libapache2-mod-wsgi-py3 python3 python3-pip python3-pil.imagetk python3-pillow mariadb-server samba git zenity pm-utils smbclient"
        operation "Installing python3 libraries." $(pip3 install django==3.2.13 2> /dev/null; pip3 install pyotp 2> /dev/null; pip3 install json 2> /dev/null; pip3 install hashlib 2> /dev/null; pip3 install base64 2> /dev/null; pip3 install qrcode 2> /dev/null; pip3 install requests 2> /dev/null; pip3 install io 2> /dev/null; pip3 install random 2> /dev/null; pip3 install binascii 2> /dev/null; pip3 install math 2> /dev/null; pip3 install os 2> /dev/null; pip3 install sys 2> /dev/null; pip3 install platform 2> /dev/null; pip3 install psutil 2> /dev/null; pip3 install mysql.connector 2> /dev/null; pip3 install pymysql 2> /dev/null; pip3 install pyscreenshot 2> /dev/null; pip3 install pysmb 2> /dev/null; pip3 install socket 2> /dev/null; pip3 install multiprocessing 2> /dev/null; pip3 install threading 2> /dev/null; pip3 install ssl 2> /dev/null; pip3 install time 2> /dev/null; pip3 install urllib3 2> /dev/null; pip3 install re 2> /dev/null; pip3 install datetime 2> /dev/null; pip3 install signal 2> /dev/null; pip3 install logging 2> /dev/null; pip3 install certifi 2> /dev/null)
        operation "Adding environtment variables." $(sed -i '/CLASSADMIN/d' /etc/environment && echo 'CLASSADMIN_HOME=/etc/ClassAdmin' >> /etc/environment && echo 'CLASSADMIN_LOG=/var/log/ClassAdmin.log' >> /etc/environment && echo 'CLASSADMIN_SSL=/etc/ClassAdmin/ssl' >> /etc/environment && sed -i '/PYTHONPATH/d' /etc/environment && echo 'PYTHONPATH=/etc/ClassAdmin' >> /etc/environment && echo "export CLASSADMIN_HOME=/etc/ClassAdmin" >> /etc/apache2/envvars && echo "export CLASSADMIN_LOG=/var/log/ClassAdmin.log" >> /etc/apache2/envvars && echo "export CLASSADMIN_SSL=/etc/ClassAdmin/ssl" >> /etc/apache2/envvars)
        operation "Installing ClassAdmin CA Bundle." $(cp ./ssl/ClassAdmin.crt /usr/local/share/ca-certificates && update-ca-certificates)
        operation "Installing apache2 modules." $(a2enmod ssl mod_wsgi rewrite)
        operation "Enabling apache2 VirtualHosts sites." $(cp -r ./apache2.conf.d/linux/ClassAdmin* /etc/apache2/sites-available/; a2ensite ClassAdminS ClassAdminS-ssl)
        server=""
        while [[ $(echo $server | grep -E -o "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}") == "" ]];
        do
        	echo -ne "\033[1;34m[?]\033[0m Which is ClassAdminS server IP address?: "
        	read server
        done
        operation "Adding dns in /etc/hosts." $(sed -i '/classadmin.server/d' /etc/hosts && echo "$server     classadmin.server" >> /etc/hosts)
        operation "Installing ClasAdminS service." $(cp ./Daemon/ClassAdminS.service /lib/systemd/system && systemctl daemon-reload && chmod 644 /lib/systemd/system/ClassAdminS.service)
        notification=""
        while [[ $notification != "true" && $notification != "false" ]];
        do
        	echo -ne "\033[1;34m[?]\033[0m Do you want that ClassAdmin service send system notifications? [true/false]: "
        	read notification
        done
        operation "Configurating notifications." $(sed -E -i "s/\"notifications\": \"(.*)\"/\"notifications\": \"$notification\"/g" ./services/ClassAdmin.conf)
        user=""
        while [[ $user == "" ]];
        do
        	echo -ne "The notifications will be execute as user...: "
        	read user
        done
        operation "Notifications will be execute as $user." $(sed -i -E "s/\"user\":(.*)/\"user\":\"$user\"/g" ./services/ClassAdmin.conf 2> /dev/null)
        operation "Creating ClassAdmin user." $(useradd -p $(openssl passwd -6 12345678) -d /home/ClassAdmin -m -k --badname ClassAdmin 2> /dev/null)
        operation "Changing permissions for ClassAdmin proyect." $(chmod o+w /var/log 2> /dev/null && chown -R root:www-data . 2> /dev/null && chmod -R g+w . 2> /dev/null && chown www-data:ClassAdmin ./transfers/.screenshots/ 2> /dev/null && chmod -R 770 ./transfers/.screenshots 2> /dev/null && chown www-data:www-data /var/log/ClassAdmin.log)
        operation "Configurating MariaDB/mySQL." $(sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/mariadb.conf.d/50-server.cnf 2> /dev/null; sed -E -i "s/(.*)max_allowed_packet(.*)=(.*)/max_allowed_packet = 1G/g" /etc/mysql/mariadb.conf.d/50-server.cnf 2> /dev/null; sed -E -i "s/(.*)max_connections(.*)=(.*)/max_connections = 1000/g" /etc/mysql/mariadb.conf.d/50-server.cnf 2> /dev/null)
        operation "Creating ClassAdmin database." $(mysql -u root -e "source ./init.sql" 2> /dev/null)
        operation "Creating ClassAdminS_Screenshots shared folder." $(echo "[ClassAdminS_Screenshots]" >> /etc/samba/smb.conf && echo "   path = /etc/ClassAdmin/transfers/.screenshots" >> /etc/samba/smb.conf && echo "   available = yes" >> /etc/samba/smb.conf && echo "   browseable = yes" >> /etc/samba/smb.conf && echo "   writable = yes" >> /etc/samba/smb.conf && echo "   guest ok = no" >> /etc/samba/smb.conf && echo "   create mask = 0770" >> /etc/samba/smb.conf && echo "   directory mask = 0770" >> /etc/samba/smb.conf && echo "   force group = www-data" >> /etc/samba/smb.conf && echo "   valid users = ClassAdmin" >> /etc/samba/smb.conf)
        operation "Adding ClassAdmin user to shared folder." $((echo 12345678; echo 12345678) | smbpasswd -s -a ClassAdmin)
        operation "Enabling ClassAdminS service in the boot." $(systemctl enable ClassAdminS)
        operation "Enabling apache2 service in the boot." $(systemctl enable apache2)
        operation "Enabling MariaDB service in the boot." $(systemctl enable mariadb)
        operation "Restarting apache2 service." $(systemctl restart apache2)
        operation "Restarting MariaDB service." $(systemctl restart mariadb)
        operation "Starting ClassAdminS service." $(systemctl start ClassAdminS)
        echo -e "\033[1;32m[+]\033[0m ClassAdminS installation completed"
else
        exit 1
fi
