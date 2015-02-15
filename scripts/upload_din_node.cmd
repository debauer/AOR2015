rsync --numeric-ids -avze ssh ../* root@%1:/home/AOR2015
ssh -l root %1 arduino --board /home/AOR2015/scripts/programm_din_node.sh