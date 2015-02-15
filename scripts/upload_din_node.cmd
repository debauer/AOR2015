
rsync --numeric-ids -avze ssh ../* root@%1:%2
ssh -l root %1 "chmod +x %2/scripts/programm_din; %2/scripts/./programm_din %2"
