#
# IOT E6756 Lab Assignment 2
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 4. (30 pts) Write a script to periodically (e.g. once per second) read
# temperature data from the Wiced Sense BLE sensor tag and display the
# temperature in Celsius on the LCD screen.
#
# Usage.
# > python A2_JSJC_#4.py BLUETOOTH_ADR
# ex:
# > python A2_JSJC_#4.py 00:10:18:01:1B:B9
#

import json
import time
import mraa
import pyupm_i2clcd as lcd
import pexpect
import sys
import datetime

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Yellow LCD
myLcd.setColor(255, 255, 0)

def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)
        pass
    return t

print "Press Ctrl+C to escape..."
try:
    # connect to device
    bluetooth_adr = sys.argv[1]
    tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
    tool.expect('\[LE\]>')
    print "Preparing to connect. You might need to press the side button..."
    tool.sendline('connect')
    # test for success of connect
    tool.expect('Connection successful')
    print ""
    print "Connected!"

    last_time = datetime.datetime.now().second
    # initial temperature
    t = 230

    while (1):
        # setup bluetooth temp sensor
        tool.sendline('char-write-req 0x2b 0x01')
        tool.sendline('char-write-req 0x2b 0x00')
        tool.expect('\[LE\]>')
        # read Bluetooth temp sensor
        tool.sendline('char-read-hnd 0x2a')
        tool.expect('descriptor: .*')
        rval = tool.after.split()
        #print "loop"
        #print rval
        now = datetime.datetime.now().second
        #print last_time
        #print now

        if rval[1] == '34':
            #print rval[6] # 6th byte
            #print rval[7] # 7th byte
            # convert to hex
            t = floatfromhex(rval[7]+rval[6])
            #print "t",t
        if (now >= last_time + 3) | (last_time >= now +3):
            last_time = now
            celsius = float(t/10.0)
            #print celsius
            # Convert to F
            fahrenheit = celsius * 9.0/5.0 + 32.0;
            # Print it in the console
            print "%.1f degrees C, or %.1f degrees F" \
            % (celsius, fahrenheit)
            myLcd.clear()        # clear
            myLcd.setCursor(0,0) # zero the cursor
            myLcd.write("%.1f degrees C" % (celsius))

except KeyboardInterrupt:
    exit
except:
    print "Error in Main Loop"
