
# flock logger 
# v0.0 14.05.18 master@owlh.net

import os
#import flockdefs
from datetime import datetime
import flockconf
conf = flockconf.get_item

def initflocklogger():
    global logfile 
    bufsize = 0 # 0 -> force flush on each write
    try: 
        logfile = file(conf("logfile"),'a',bufsize)
    except Exception as inst:
        print "Error - %s" % str(inst)

def killflocklogger():
    flocklogger ("Closing log output")
    global logfile
    logfile.close()

def flocklogger(text, level="INFO", proc="flock", id=os.getpid()):
    global logfile
    logfile.write(datetime.utcnow().strftime('%a %d %b %Y %H:%M:%S.%f') + " [" + proc + "] (" + str(id) +") [" + level+ "]: " + text + "\n")

logfile = ""
initflocklogger()
