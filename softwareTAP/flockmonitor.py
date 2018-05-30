#flock monitor
#v0.0 16-05-18 master@owlh.net

import re

import flocklogger
import flockssh
import flockconf

flogger = flocklogger.flocklogger
conf = flockconf.get_item

def check_owl_alive (owl):
    flogger ("check owl %s is alive" % owl["name"])
    alive, ssh = flockssh.check_owl_alive(owl)
    return alive, ssh

def get_status_cpu (owl, cpu):
    if not re.search("\d+",cpu):
        return True
    flogger ("check owl %s CPU" % owl["name"])
    max_cpu = conf("max_cpu")
#    if float(cpu) > float(conf["max_cpu"]): 
    if float(cpu) > float(max_cpu): 
        flogger ("SNIFFER -> too much cpu %s %% (max %s %%) on owl %s" % (cpu, max_cpu, owl["name"]), "WARNING")
        return False
    return True

def get_status_mem (owl,mem):
    if not re.search("\d+",mem):
        return True
    flogger ("check owl %s MEM" % owl["name"])
    max_mem = conf("max_mem")
#    if float(cpu) > float(conf["max_mem"]): 
    if float(mem) > float(max_mem): 
        flogger ("SNIFFER -> too much mem %s %% (max %s %%) on owl %s " % (mem, max_mem, owl["name"]), "WARNING")
        return False
    return True


def get_status_sniffer (owl, ssh):
    flogger ("check owl %s sniffer status" % owl["name"])
    running, pid, cpu, mem = flockssh.get_status_sniffer(owl, ssh)
    cpustatus = get_status_cpu (owl,cpu)
    memstatus = get_status_mem (owl,mem)
    storagestatus = get_status_storage(owl,ssh)
    flogger ("check owl %s ==>> CPU: %s, MEM: %s, STO: %s sniffer status" % (owl["name"],cpustatus,memstatus,storagestatus))
    if cpustatus and memstatus and storagestatus:
        return running, True
    return running, False

def get_status_storage (owl,ssh):
    pcap_path = conf("pcap_path")
    flogger ("check owl %s storage -> pcap path: %s" % (owl["name"],pcap_path))
#    df -h /home/jose --output=source,pcent | grep -v Filesystem
    status, storage, path = flockssh.get_status_storage(owl, ssh, pcap_path)
    if status:
        if int(storage) > int(conf("max_storage")):
            flogger ("PCAP -> too much storage used %s %% (max %s %%) partition: %s on owl %s " % (storage, conf("max_storage"), path, owl["name"]), "WARNING")
            return False
        return True
    return False

def run_sniffer (owl,ssh):
    flogger ("run sniffer on owl %s" % owl["name"])
    flockssh.run_sniffer(owl, ssh, conf("default_interface"),conf("capture_time"),conf("pcap_path"),conf("filter_path"), conf("owlh_user"))

def stop_sniffer (owl, ssh):
    flogger ("STOP sniffer on owl %s" % owl["name"])
    flockssh.stop_sniffer(owl, ssh)

def get_file_list (owl,ssh):
    flogger ("get file list on owl %s" % owl["name"])
    file_list = flockssh.get_file_list(owl,ssh, conf("pcap_path"))
    sftp = ssh.open_sftp()
    for file in file_list:
        if re.search("\.pcap",file):
            owner_owlh(owl, ssh, conf("pcap_path")+file)
            transport_file(owl, sftp, conf("pcap_path")+file, conf("local_pcap_path")+file)
            remove_file(owl, sftp, conf("pcap_path")+file)

def owner_owlh (owl, ssh, file_remote):
    flogger ("set %s as owner of file %s from owl %s" % (conf("owlh_user"), file_remote, owl["name"]))
    flockssh.owner_owlh(owl, ssh, file_remote, conf("owlh_user"))

def transport_file (owl, sftp, file, local_path):
    flogger ("get file %s from owl %s" % (file, owl["name"]))
    flockssh.transport_file(owl, sftp, file, local_path)

def remove_file (owl, sftp, file):
    flogger ("remove file %s from owl %s" % (file, owl["name"]))
    flockssh.remove_file(owl, sftp, file)