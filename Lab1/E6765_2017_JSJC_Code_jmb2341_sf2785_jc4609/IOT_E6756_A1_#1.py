#
# IOT E6756 Lab Assignment 1
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 1. (50pts) Connect a buzzer (from the Grove Starter Kit) to one of the DIO
# pins of the Intel Edison. Design a code such that the buzzer beeps for a
# finite time duration upon system startup, ie, every time you switch on the
# Intel Edison the a beeping buzzer indicates startup.
#
# /etc/init.d/startup.sh
#
# #!/bin/sh
# sleep 30
# python /home/root/Lab1/A1/IOT_E6756_A1_#1
# python /home/root/Lab1/A1/IOT_E6756_A1_#2
# exit 0
#
# Made an executable `chmod u+x startup.sh`
# Initialized as service `update-rc.d startup.sh defaults`
#

import mraa
import time

# initialize variables
buzz_pin_number=6
x = 0

# Configuring the  buzzer as GPIO interfaces
buzz = mraa.Gpio(buzz_pin_number)

# Configuring the switch and buzzer as input & output respectively
buzz.dir(mraa.DIR_OUT)

print "Press Ctrl+C to escape..."
try:
        while x < 3:
        # buzzer beeps for 3 cycles of the while loop
                buzz.write(1)   # switch on the buzzer
                time.sleep(0.2) # puts system to sleep for 0.2sec before switching
                buzz.write(0)   # switch off buzzer
                x+=1            # increment x

except KeyboardInterrupt:
        exit
