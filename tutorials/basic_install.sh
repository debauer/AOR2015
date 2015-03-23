# sd card expanden ned vergessen!

# basic
	sudo aptitude update
	sudo aptitude upgrade
	sudo su
	cd 
	cat /home/pi/.bashrc >> .bashrc
	aptitude install htop screen mc

# elasticsearch 1.4.4 - tested on rpi2

	mkdir /usr/share/elasticsearch
	cd /usr/share/elasticsearch
	curl -L -O https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.4.tar.gz
	
	nano config/elasticsearch.yml
	# edit 
	# #path.data: /path/to/data -> path.data: /mnt/ssd0/elasticdata
	
	# in screen
	cd elasticsearch-1.4.4/bin
	./elasticsearch

# mongodb 2.1.1 - tested on rpi2
# https://github.com/RickP/mongopi
	git clone https://github.com/svvitale/mongo4pi
	cd mongo4pi
	./install.sh

# nodejs v0.10.37 - tested on rpi2
	curl -sL https://deb.nodesource.com/setup | sudo bash -
	sudo apt-get install -y build-essential python-dev python-rpi.gpio nodejs
	

# samba
	aptitude install samba samba-common-bin
	nano /etc/samba/smb.conf
	# edit 
	# #security = user -> security = user

#echo "deb http://mirrordirector.raspbian.org/raspbian/ jessie main contrib non-free rpi" > /etc/apt/sources.list.d/jessie.list

# sudo aptitude install build-essential libboost-filesystem-dev libboost-program-options-dev libboost-system-dev libboost-thread-dev scons libboost-all-dev python-pymongo git


#git clone https://github.com/4commerce-technologies-AG/meteor.git
#cd meteor
#cp -a /bin/. /usr/bin/
#cp -a /lib/. /usr/lib
#cp -a /include/. /usr/include
