#!/usr/bin/env python3

# owlh controller
# v0.0 14.05.18 master@owlh.net

import time
import os
import sys

# own libs
import flocklogger 
import flockmanager
import flockinventory


flogger = flocklogger.flocklogger

def main():
    flogger ("init","INFO")
    if not flockmanager.amirunning():
        while not flockmanager.killme():
            flockinventory.run()
            time.sleep (10) # Just for testing, deleting in a while
        flockmanager.byebye()

main()