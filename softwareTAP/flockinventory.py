# flock inventory
# v0.0 14-05-18 master@owlh.net

#import flockdefs
import json
import flocklogger 
import flockmonitor
import flockconf

flogger = flocklogger.flocklogger
conf = flockconf.get_item


def loadinventory():
    with open(conf("inventory")) as json_data:
        owlhs = json.load(json_data)
    return owlhs

def printinventory(owlhs):
    for owlh in owlhs: 
        print owlh["name"]

def run():
    owls = loadinventory()
    for owl in owls: 
        flogger("checks for owl name -> %s, owl ip -> %s" % (owl["name"], owl["ip"]))
        alive, ssh = flockmonitor.check_owl_alive(owl)
        if alive:
            flogger(">>> as Owl name-> %s, is ALIVE, will check status" % (owl["name"]))
            running, status_ok = flockmonitor.get_status_sniffer(owl,ssh)
            flogger (">>> Running: %s, Status: %s " % (running, status_ok))
            if running:
                if not status_ok:
                    flockmonitor.stop_sniffer(owl,ssh)
            elif status_ok:
                flockmonitor.run_sniffer(owl,ssh)
            flockmonitor.get_file_list(owl, ssh)
            ssh.close()


