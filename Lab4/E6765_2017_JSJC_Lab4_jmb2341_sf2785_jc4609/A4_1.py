import mraa
import time
import math

# Create the temperature sensor object using AIO pin 0
tempSensor = mraa.Aio(0)

# Setup aws
topic = 'mtaSub'
topic_arn = arn:aws:sns:us-east-1:811222862937:mtaSub

def email():
    try:

        return True
    except KeyboardInterrupt:
            exit
    except:
        print "Error with Email"

def sms():
    try:

        return True
    except KeyboardInterrupt:
            exit
    except:
        print "Error with SMS"


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
                    e = email(item)
                    s = sms(item)
                    # print result of attempt
                    print "email %s, sms %s" % (e,s)

                    time.sleep(10)        # pause 10 seconds
except KeyboardInterrupt:
        exit

##########################

import boto.sns
import logging

logging.basicConfig(filename="sns-email-sub.log", level=logging.DEBUG)

c = boto.sns.connect_to_region("us-east-1")

topicarn = "$TOPIC_ARN"
emailaddress1 = "some email"
emailaddress2 = "some other email"

subscription1 = c.subscribe(topicarn, "email", emailaddress1)
subscription2 = c.subscribe(topicarn, "email", emailaddress2)

print subscription1
print subscription2

###########

#!//opt/boxen/homebrew/bin/python

import boto.sns
import json


REGION = 'us-west-2'
TOPIC  = '<ARN>'
URL    = '<Body of Message in this example I used a url>'

conn = boto.sns.connect_to_region( REGION )
pub = conn.publish( topic = TOPIC, message = URL )

##########################

import boto.sns
import logging

logging.basicConfig(filename="sns-publish.log", level=logging.DEBUG)

c = boto.sns.connect_to_region("us-east-1")

topicarn = "$TOPIC_ARN"
message = "hello Mr"
message_subject = "trialBotoTRopic"

publication = c.publish(topicarn, message, subject=message_subject)

print publication
Raw
