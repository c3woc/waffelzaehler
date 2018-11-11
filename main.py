#!/usr/bin/python3
# -*- coding: utf-8 -*
#
# Waffelzahler
# https://github.com/ToolboxBodensee/waffelzaehler
#
import RPi.GPIO as GPIO # raspi gpio-pins
from time import time, sleep # fuer zeitmessung und pausen
from sys import argv # fuer die kommandozeilenargumente

# Pins für die Sensoren
waffel = [36, 37, 38, 40]

debug = False

def setup:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    for key in waffel.items():
         GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
         if debug: print("GPIOs eingestellt")

            

for i in argv:
    if i in ["--help", "-h", "/h", "/help", "?", "h"]:
        print("Moegliche Befehle:\n\t --help \t- Zeigt diese Hilfe an")
        print("\t--debug\t- Debug Modus...")
        print("\n")
        exit()
    elif i == "--debug":
        debug = True
        print("Debug Modus")
                                                                                                                                
