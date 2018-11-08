if  [[ $(sudo /sbin/ip link list owlh) =~ ^[0-9] ]] ; then
  echo "owlh interface exists - nothing to do"
  exit 0
fi
sudo echo 'Creating owlh Interface...'
sudo echo 'dummy' > /etc/modules-load.d/dummy.conf
sudo echo 'install dummy /sbin/modprobe --ignore-install dummy; /sbin/ip link set name owlh dev dummy0 ' > /etc/modprobe.d/dummy.conf

sudo echo "
NAME=owlh
DEVICE=owlh
ONBOOT=yes
TYPE=Ethernet
NM_CONTROLLED=no
" > /etc/sysconfig/network-scripts/ifcfg-owlh

sudo /sbin/modprobe --ignore-install dummy
sudo /sbin/ip link add owlh type dummy
sudo ifup owlh
sudo echo "NOZEROCONF=yes" >> /etc/sysconfig/network
sudo /sbin/ip link list owlh
sudo echo 'Created owlh interface. Enjoy.'

