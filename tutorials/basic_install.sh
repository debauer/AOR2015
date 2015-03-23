# sd card expanden ned vergessen!

# basic
	sudo aptitude update
	sudo aptitude upgrade
	sudo su
	cd 
	cat /home/pi/.bashrc >> .bashrc
	aptitude -y install htop screen mc python-pip
	adduser debauer

# elasticsearch 1.4.4 - tested on rpi2 - wird erstmal nicht mehr gebraucht

	mkdir /usr/share/elasticsearch
	cd /usr/share/elasticsearch
	curl -L -O https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.4.tar.gz
	
	echo "path.data: /mnt/ssd0/elasticdata" > config/elasticsearch.yml
	
	#mv elasticsearch-1.4.4 elasticsearch
	cd bin
	./elasticsearch -d 
	echo "@reboot /usr/share/elasticsearch/bin/elasticsearch -d" > /etc/crontab

# mongodb 2.1.1 - tested on rpi2
# https://github.com/RickP/mongopi
	cd /home/pi
	git clone https://github.com/svvitale/mongo4pi
	cd mongo4pi
	./install.sh

# nodejs v0.10.37 - tested on rpi2
	curl -sL https://deb.nodesource.com/setup | sudo bash -
	aptitude -y install build-essential python-dev python-rpi.gpio nodejs
	

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

# aor_daemon
	cd /home/debauer/AOR2015/py
	pip install -r requirements.txt

# apache 2
	aptitude install apache2

# graphite - verworfen
#	cd /home/debauer/AOR2015/py
#	pip install -r requirements.txt
#	cd /opt/graphite/conf/
#   ... 
  
# influxdb
	cd /home/pi
	wget http://demos.pihomeserver.fr/influxdb_0.8.6_armhf.deb
	dpkg --install influxdb_0.8.6_armhf.deb
	service influxdb start

# grafana
	cd /var/www
	wget http://grafanarel.s3.amazonaws.com/grafana-1.9.1.tar.gz
	tar -xzf grafana-1.9.1.tar.gz grafana-1.9.1
	mv grafana-1.9.1 grafana
	cd grafana
	cat /home/debauer/AOR2015/configs/grafana.js >> config.js
