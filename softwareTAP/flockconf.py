# flock conf
# v0.0 14-05-18 master@owlh.net

configfile = "/etc/owlh/owlh.conf" # this must be in other place.

import json

conf = ""

def loadconf():
    with open(configfile) as conf_data:
        global conf 
        conf = json.load(conf_data)

def get_item(item):
    global conf
    return conf[item]

def printconf():
    global conf
    for item in conf: 
        print item + " -> " + conf[item]

loadconf()