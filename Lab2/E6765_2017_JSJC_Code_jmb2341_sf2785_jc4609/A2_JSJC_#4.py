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
# > A2_JSJC_#4.py BLUETOOTH_ADR
#

import json
import time
import mraa
import pyupm_i2clcd as lcd
import pexpect
import sys

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

def calcTmpTarget(objT, ambT):
    m_tmpAmb = ambT/128.0
    Vobj2 = objT * 0.00000015625
    Tdie2 = m_tmpAmb + 273.15
    S0 = 6.4E-14            # Calibration factor
    a1 = 1.75E-3
    a2 = -1.678E-5
    b0 = -2.94E-5
    b1 = -5.7E-7
    b2 = 4.63E-9
    c2 = 13.4
    Tref = 298.15
    S = S0*(1+a1*(Tdie2 - Tref)+a2*pow((Tdie2 - Tref),2))
    Vos = b0 + b1*(Tdie2 - Tref) + b2*pow((Tdie2 - Tref),2)
    fObj = (Vobj2 - Vos) + c2*pow((Vobj2 - Vos),2)
    tObj = pow(pow(Tdie2,4) + (fObj/S),.25)
    tObj = (tObj - 273.15)
    print "%.2f C" % tObj

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

    while (1):
        # setup bluetooth temp sensor
        tool.sendline('char-write-req 0x2b 0x01')
        tool.sendline('char-write-req 0x2b 0x00')
        tool.expect('\[LE\]>')
        # read Bluetooth temp sensor
        tool.sendline('char-read-hnd 0x2a')
        tool.expect('descriptor: .*')
        rval = tool.after.split()
        if rval[1] == '34':
            #print rval[6] # 6th byte
            #print rval[7] # 7th byte
            # convert to hex
            t1 = floatfromhex(rval[6])
            t2 = floatfromhex(rval[7])
            celsius = (t1 + t2)/10
            # Convert to F
            fahrenheit = celsius * 9.0/5.0 + 32.0;
            # Print it in the console
            print "%d degrees C, or %d degrees F" \
            % (celsius, fahrenheit)
            myLcd.clear()        # clear
            myLcd.setCursor(0,0) # zero the cursor
            myLcd.write("%d degrees C" % (celsius))

except KeyboardInterrupt:
    exit
except:
    print "Error in Main Loop"
