#
# IOT E6756 Lab Assignment 4
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# Question 1 (20 pts)
# Using a temperature sensor, send subscribers the temperature of the Edison's
# surroundings, by SMS & email, using only Amazon SNS (do not use the code you
# developed in Lab 1 for email). You need not have code to add new subscribers,
# you may use a predefined list.
#

import mraa
import time
import math
import boto3
import logging
from utils import aws

# Create the temperature sensor object using AIO pin 0
tempSensor = mraa.Aio(0)

# Get the service resource.
client = aws.getClient('sns', 'us-east-1')

def publish(subject,message):
    try:
        response = client.publish(
            TopicArn='arn:aws:sns:us-east-1:811222862937:mtaSub',
            #TargetArn='string',
            #PhoneNumber='string',
            Message=str(message),
            Subject=str(subject),
            #MessageStructure='string',
            #MessageAttributes={
                #'string': {
                    #'DataType': 'string',
                    #'StringValue': 'string',
                    #'BinaryValue': b'bytes'
                #}
            #}
        )
        return True
    except KeyboardInterrupt:
            exit
    except:
        print "Error Publishing"


print "Press Ctrl+C to escape..."
try:
        while (1):
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
            # Convert to F
            fahrenheit = celsius * 9.0/5.0 + 32.0;
            # Print it in the console
            print "%d degrees C, or %d degrees F" \
            % (celsius, fahrenheit)

            # publish message to subscrivers here
            item = {'fahrenheit':fahrenheit, 'celsius':celsius}
            publish('temperature',item)

            time.sleep(10)        # pause 10 seconds
except KeyboardInterrupt:
        exit
except:
    print "Error in Main Loop"
