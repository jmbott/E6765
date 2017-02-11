#
# IOT E6756 Lab Assignment 1
#
# Group:  JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 3. (40pts) Design a simple system, using a switch (the Grove button) &
# temperature sensor from the Starter Kit, such that every time you press the
# switch, it displays the temperature on your LCD screen.
#

import mraa
import time
import pyupm_i2clcd as lcd

# initialize switch variable
switch_pin_number=8

# Configuring the switch as GPIO interfaces
switch = mraa.Gpio(switch_pin_number)

# Create the temperature sensor object using AIO pin 0
tempSensor = mraa.Aio(0)

# Configuring the switch as an input
switch.dir(mraa.DIR_IN)

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Yellow LCD
myLcd.setColor(255, 255, 0)

print "Press Ctrl+C to escape..."
try:
        while (1):
                if (switch.read()):     # check if switch pressed
                # Read the temperature, printing both the Celsius and
                # equivalent Fahrenheit temperature
			            temp = tempSensor.read()
                        # ADC has output range 0 to 1023
                        # Temp sensor works from -40C to 125C,
                        # 165 degree range offset by 40 degrees C
                        # 1024/165 = 6.2
                        celsius = temp/6.2 - 40;
                        fahrenheit = celsius * 9.0/5.0 + 32.0;
                        # Print it in the console
                        print "%d degrees C, or %d degrees F" \
                        % (celsius, fahrenheit)
                        myLcd.clear()        # clear
                        myLcd.setCursor(0,0) # zero the cursor
                        myLcd.write("%d degrees C" % (celsius))
			            time.sleep(1)        # pause
                        myLcd.clear()        # clear
                        myLcd.setCursor(0,0) # zero the cursor
                        myLcd.write("%d degrees F" % (fahrenheit))
                        time.sleep(1)        # pause
except KeyboardInterrupt:
        exit
