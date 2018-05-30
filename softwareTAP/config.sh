#!/bin/bash
# configure owlhmaster
# v0.0 22.05.18 master@owlh.net
# tested - Centos7

# get my ip 
# ip a | grep "inet " | grep -v 127.0.0.1 | awk -F '[[:space:]/]' '{print $6}'

sudo adduser owlh
#echo "create owl user ssh folder"
#sudo -u owlh mkdir /home/owlh/.ssh
#echo "setting ssh folder permissions"
#sudo -u owlh chmod 700 /home/owlh/.ssh
#echo "create authorized keys file"
#sudo -u owlh touch /home/owlh/.ssh/authorized_keys
#echo "setting authorized keys permissions"
#sudo -u owlh chmod 600 /home/owlh/.ssh/authorized_keys
echo "create owlmaster key"
sudo -u owlh ssh-keygen -t rsa -f /home/owlh/.ssh/owlhmaster -N ""
sudo -u owlh chmod 600 /home/owlh/.ssh/owlhmaster
sudo -u owlh chmod 600 /home/owlh/.ssh/owlhmaster.pub


echo "create owlh folder structure"
echo "create /etc/owlh"
sudo mkdir /etc/owlh
sudo chown owlh /etc/owlh
sudo chgrp owlh /etc/owlh
echo "create /var/log/owlh log"
sudo mkdir /var/log/owlh
sudo chown owlh /var/log/owlh
sudo chgrp owlh /var/log/owlh
echo "create /usr/share/owlh data"
sudo mkdir /usr/share/owlh
sudo mkdir /usr/share/owlh/in_queue
sudo mkdir /usr/share/owlh/in_progress
sudo mkdir /usr/share/owlh/out_queue
sudo chown -R owlh /usr/share/owlh
sudo chgrp -R owlh /usr/share/owlh
echo "create /opt/owlh src"
sudo mkdir /opt/owlh
sudo chown -R owlh /opt/owlh
sudo chgrp -R owlh /opt/owlh

sudo curl -o /etc/owlh/owlh.conf https://raw.githubusercontent.com/owlh/flockcontroller/master/conf.json
sudo curl -o /etc/owlh/inventory.conf https://raw.githubusercontent.com/owlh/flockcontroller/master/inventory.json
sudo curl -o /opt/owlh/flockanalyzer.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flockanalyzer.py
sudo curl -o /opt/owlh/flockcontroller.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flockcontroller.py 
sudo curl -o /opt/owlh/flockinventory.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flockinventory.py 
sudo curl -o /opt/owlh/flockkiller.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flockkiller.py 
sudo curl -o /opt/owlh/flocklogger.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flocklogger.py 
sudo curl -o /opt/owlh/flockmanager.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flockmanager.py 
sudo curl -o /opt/owlh/flockmonitor.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flockmonitor.py 
sudo curl -o /opt/owlh/flockssh.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flockssh.py 
sudo curl -o /opt/owlh/flockconf.py https://raw.githubusercontent.com/owlh/flockcontroller/master/flockconf.py

if ! sudo yum list installed epel-release ; then
    sudo yum --enablerepo=extras install epel-release
fi

if ! sudo yum list installed tcpreplay ; then
    sudo yum -y install tcpreplay
fi

if ! sudo yum list installed pyhton-pip ; then
    sudo yum -y install python-pip
fi

if ! sudo pip show paramiko; then
    pip install paramiko
fi



