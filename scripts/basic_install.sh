# sd card expanden ned vergessen!

# basic
	sudo aptitude update
	sudo aptitude upgrade
	sudo su
	cd 
	cat /home/pi/.bashrc >> .bashrc
	aptitude -y install htop screen mc python-pip
	adduser debauer


# USB fix
	echo "max_usb_current=1" >> /boot/config.txt

# samba
	aptitude -y install samba samba-common-bin

	echo "security = user" > nano /etc/samba/smb.conf
	sed -i 's/#security = user/security = user/g' /etc/samba/smb.conf
	echo "[debauer]" > /etc/samba/smb.conf
	echo "path = /home/debauer" > /etc/samba/smb.conf
	echo "writeable = yes" > /etc/samba/smb.conf
	echo "guest ok  = no" > /etc/samba/smb.conf

	cd /home/debauer
	git clone https://github.com/debauer/AOR2015
	chown debauer:debauer * -R

# rebooooten
	reboot