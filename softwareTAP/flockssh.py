#flockssh 
#v0.0 16-05-18 master@owlh.net


import paramiko
import re
from subprocess import call


import flocklogger
import flockconf

conf = flockconf.get_item
flogger = flocklogger.flocklogger


def run_cmd(cmd, ssh):
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = ""
        for l in stdout :
            output = l.strip()
        for l in stderr:
            print("stderr : %s" % l.strip())
        return True, output
    except Exception as inst:
        flogger("Oops!  there was a problem: %s" % str(inst),"WARNING")
        return False, ""

def run_cmd_bg(cmd, ssh):
    try:
        channel = ssh.get_transport().open_session()
        flogger("will run command: %s" % cmd,"INFO")
        stdin, stdout, stderr = channel.exec_command(cmd)
        flogger("will run command DONE: %s" % cmd,"INFO")
        output = ""
        for l in stdout:
            output = l.strip()
            print("stdout : %s" % l.strip())
        for l in stderr:
            print("stderr : %s" % l.strip())
        channel.close()
        return True, output
    except Exception as inst:
        flogger("Oops!  there was a problem: %s" % str(inst),"WARNING")
        channel.close()
        return False, ""



def owl_connect(owl):
    owl_user=conf("owlh_user")
    owl_key=conf("owlh_user_key")
    owl_ip=owl["ip"]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    try:
        ssh.connect(owl_ip, username=owl_user, key_filename=owl_key)
    except Exception as inst:
        flogger("Oops!  there was a problem: %s" % str(inst),"WARNING")
        return False, ""
    return True, ssh

def get_status_sniffer(owl,ssh):
    flogger("check if sniffer is working in owl %s (%s)" % (owl["name"], owl["ip"]))
    cmd='top -b -n1 | grep -v sudo | grep tcpdump | awk \'{print $1 "," $9 "," $10}\''
    output = ""
    status, output = run_cmd(cmd, ssh)
    if re.search("\d+,\d+\.\d+,\d+\.\d+",str(output)):
        pid, cpu, mem = output.split(",")
        if int(pid):
            flogger("sniffer is working in owl %s (%s) with pid %s, CPU %s, MEM %s" % (owl["name"], owl["ip"],pid, cpu, mem))
            return True, pid, cpu, mem
    flogger("sniffer NOT working in owl %s (%s)" % (owl["name"], owl["ip"]))
    return False, "", "", ""

def check_owl_alive(owl):
    flogger("check if owl %s (%s) is alive" % (owl["name"], owl["ip"]))
    alive, ssh = owl_connect(owl)
    if alive:
        flogger("owl %s (%s) is alive" % (owl["name"], owl["ip"]))
#        cmd='pwd; ls; date'
#        print('\n test 1\n cmd %s\n' % cmd)
#        run_cmd(cmd, ssh)
        return True, ssh
    flogger("owl %s (%s) is NOT alive" % (owl["name"], owl["ip"]))
    return False, ""

def get_status_storage(owl,ssh,folder):
#   df: '/home/jose/manolo': No such file or directory
    flogger("check if storage is OK in owl %s (%s)" % (owl["name"], owl["ip"]))
    cmd='df -h %s --output=source,pcent | grep -v Filesystem | awk \'{print $1","$2}\'' % folder
    output = ""
    status, output = run_cmd(cmd, ssh)
    if re.search("[^,]+,\d+%",str(output)):
        regx = re.match("([^,]+),(\d+)%",output)
        flogger("PCAP storage used in owl %s (%s) is %s -> %s %%" % (owl["name"], owl["ip"],regx.group(1), regx.group(2)))
        return True, regx.group(2), regx.group(1)
    flogger("can't find %s in owl %s (%s)" % (folder, owl["name"], owl["ip"]))
    return False, "", ""

def run_sniffer (owl,ssh,interface,capture,pcap_path,filter_path,user): 
    flogger("starting traffic collector on %s (%s)" % (owl["name"], owl["ip"]))
    cmd = 'nohup sudo tcpdump -i %s -G %s -w %s`hostname`-%%y%%m%%d%%H%%M%%S.pcap -F %s -z %s >/dev/null 2>&1 &' % (interface, capture, pcap_path, filter_path, user)
    output = ""
    run_cmd_bg(cmd, ssh)

def stop_sniffer (owl, ssh):
    cmd = "ps -ef | grep -v grep | grep tcpdump | awk '{printf $2\",\"}'"
    output = ""
    status, output = run_cmd(cmd,ssh)
    if re.search("[^,]+,",output):
        output = re.sub(","," ",output)
        flogger("stopping traffic collector process %s on %s (%s)" % (output, owl["name"], owl["ip"]))
        cmd = "sudo kill -9 " + output
        status, output = run_cmd(cmd,ssh)
        return status, output
        flogger("stopping traffic collector => nothing to stop  on %s (%s)" % (output, owl["name"], owl["ip"]))

def get_file_list (owl, ssh, folder):
    cmd = "find %s*.pcap -maxdepth 0 -type f -mmin +1|sed 's#.*/##'| awk '{printf $1\",\"}'" % folder
    status, output = run_cmd(cmd,ssh)
    files = output.split(",")
    return files

def owner_owlh (owl, ssh, file_remote, user): 
    if re.search("\.pcap",file_remote):
        flogger("setting %s as owner of %s from %s" % (user, file_remote, owl["name"]))
        cmd = "sudo chown %s %s" % (user, file_remote)
        status, output = run_cmd(cmd,ssh)

def transport_file (owl, sftp, file_remote, file_local):
    if re.search("\.pcap",file_remote):
        flogger("collecting: %s to %s" % (file_remote, file_local))
        sftp.get(file_remote, file_local)

def remove_file (owl, sftp, file_remote):
    if re.search("\.pcap",file_remote):
        flogger("cleaning: %s from %s" % (file_remote, owl["name"]))
        sftp.remove(file_remote)

def nothing():
    scp_opt=""
    cmd='scp -q ' + scp_opt + ' -o NumberOfPasswordPrompts=1 -o StrictHostKeyChecking=no %s root@%s:~/; echo $? done.' % ( test_script, priv_ip )
    print('\n test 2\n cmd %s\n' % cmd)
    run_cmd(cmd)

    scp_opt="-v"
    cmd='scp -q ' + scp_opt + ' -o NumberOfPasswordPrompts=1 -o StrictHostKeyChecking=no %s root@%s:~/; echo $? done.' % ( test_script, priv_ip )
    print('\n test 3\n cmd %s\n' % cmd)
    run_cmd(cmd)