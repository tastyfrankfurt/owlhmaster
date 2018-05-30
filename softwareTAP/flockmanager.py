import os.path
import signal

import flockkiller
#import flockdefs
import flocklogger 
import flockconf

conf = flockconf.get_item
flogger = flocklogger.flocklogger
killer = flockkiller.flockKiller()

def killme():
    return killer.killme

def registerflock():
    flogger (str(os.getpid()))
    file(conf("pidfile"), 'w').write(str(os.getpid()))

def amirunning():
    if os.path.isfile(conf("pidfile")):
        flogger ("I'm running, we don't need two of us, exiting...")
        flogger ("If you think I'm not running, please check process list and %s" % conf("pidfile"))
        return True
    registerflock()
    return False

def byebye():
    flogger ("Time to go home. See you soon")
    flocklogger.killflocklogger()
    os.unlink(conf("pidfile"))

# Just as a remainder. If pid file is in place, try to show if the process is running for sure.
def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True