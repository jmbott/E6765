#
# IOT E6756 Lab Assignment 2
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 4. (30 pts) Write a script to periodically (e.g. once per second) read
# temperature data from the Wiced Sense BLE sensor tag and display the
# temperature in Celsius on the LCD screen.
#

import json
import time
import mraa
import pyupm_i2clcd as lcd

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Yellow LCD
myLcd.setColor(255, 255, 0)

print "Press Ctrl+C to escape..."
try:
    while (1):

        # read Bluetooth temp sensor in celsius


        myLcd.clear()        # clear
        myLcd.setCursor(0,0) # zero the cursor
        myLcd.write("%d degrees C" % (celsius))
        # Convert to F
        fahrenheit = celsius * 9.0/5.0 + 32.0;
        # Print it in the console
        print "%d degrees C, or %d degrees F" \
        % (celsius, fahrenheit)
        time.sleep(1)

except KeyboardInterrupt:
    exit
except:
    print "Error"
    return False
