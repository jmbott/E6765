#
# Populates out.csv with temp values from sensor
#
# print open('out.csv', 'rt').read()
#

import mraa
import time
import math
import os.path

# Create the temperature sensor object using AIO pin 0
tempSensor = mraa.Aio(0)

# create random number in temp range
def temp():
    try:
        # Read the temperature, printing both the Celsius and
        # equivalent Fahrenheit temperature
        temp = tempSensor.read()
        # ADC has output range 0 to 1023
        # Temp sensor works from -40C to 125C,
        # 165 degree range ofset by 40 degrees C
        R = 1023.0/temp - 1.0
        R = 100000.0*R
        # thermister B=4275
        celsius = 1.0/(math.log10(R/100000.0)/4275+1/298.15)-273.15
        fahrenheit = celsius * 9.0/5.0 + 32.0
        # Print it in the console
        print "%d degrees C, or %d degrees F" \
        % (celsius, fahrenheit)
        # add to list and return
        # ts = time.time()
        ts = time.strftime("%b %d %H:%M:%S")
        t = [ts, celsius, fahrenheit]
        return t
    except KeyboardInterrupt:
            exit
    except:
        print "Temp Fetch Error"

print "Press Ctrl+C to escape..."
try:
if os.path.exists('out.csv'):
    pass
else:
    with open('out.csv','wb') as fout:
        writer = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['timestamp','celsius','fahrenheit'])
while True:
    with open('out.csv','a') as fout:
        writer = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
        # writer.writerow(['timestamp','celsius','fahrenheit'])
        table = temp()
        writer.writerow(table)
        time.sleep(1)
except KeyboardInterrupt:
        exit
except:
    print "Error in random.py"
