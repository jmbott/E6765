#
# IOT E6756 Lab Assignment 2
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 3. (30pts) After setting up your Amazon Web Services as described in the
# document, design a system that shall stream temperature readings from your
# temperature sensor to your cloud DynamoDB database. Every time you press
# the switch, it should shift to using the Amazon Kinesis service. If you
# press the switch again, it should revert to storing data in the database
# and so on. Use the LCD display to indicate your current mode of operation.
# Your data fields could be the measurement-iteration, temperature & timestamp.
#

import boto
import boto.dynamodb2
import json
import argparse
import ast
import time
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
import mraa
import pyupm_i2clcd as lcd
import math

# initialize switch variable
switch_pin_number=8

# Configuring the switch as GPIO interfaces
switch = mraa.Gpio(switch_pin_number)

# Configuring the switch as an input
switch.dir(mraa.DIR_IN)

# Create the temperature sensor object using AIO pin 0
tempSensor = mraa.Aio(0)

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Yellow LCD
myLcd.setColor(255, 255, 0)

# AWS Account Information
ACCOUNT_ID = '811222862937'
IDENTITY_POOL_ID = 'us-east-1:366af791-82c4-490a-8b3e-157a7b007ba2'
ROLE_ARN = 'arn:aws:iam::811222862937:role/Cognito_edisonDemoKinesisUnauth_Role'

# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])

# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

# Prepare DynamoDB client
client_dynamo = boto.dynamodb2.connect_to_region(
    'us-east-1',
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)

# Create the DynamoDB table.
def create_table(name,hashkey,rangekey):
    try:
        table = Table.create(name, schema=[HashKey(hashkey),RangeKey(rangekey)], connection=client_dynamo)
        print 'writing...'
        time.sleep(12)
        return True
    except KeyboardInterrupt:
        exit

# Create DynamoDB item.
def create_item(name, item):
    # name must be string
    # item must be dict
    try:
        table = Table(name, connection=client_dynamo)
        table.put_item(data=item)
        return True
    except KeyboardInterrupt:
        exit

print "Press Ctrl+C to escape..."
try:
    create_table('temp_stream','num','temp_c','timestamp')
    while (1):
        # current mode of operation
        myLcd.clear()        # clear
        myLcd.setCursor(0,0) # zero the cursor
        myLcd.write("Writing to Database...")
        # stream temperature readings from your temperature sensor
        # to your cloud DynamoDB database

        # Read temperature here in celsius
        temp = tempSensor.read()
        # ADC has output range 0 to 1023
        # Temp sensor works from -40C to 125C,
        # 165 degree range ofset by 40 degrees C
        R = 1023.0/temp - 1.0
        R = 100000.0*R
        # thermister B=4275
        c = 1.0/(math.log10(R/100000.0)/4275+1/298.15)-273.15

        # number of readings: n

        # timestamp of reading: t

        # Convert to F
        f = c * 9.0/5.0 + 32.0;
        # Print it in the console
        print "%d degrees C, or %d degrees F" \
        % (celsius, fahrenheit)
        # Post temperature to DynamoDB
        create_item('temp_stream',{'num':n, 'temp_c':c, 'timestamp':t})


        if (switch.read()):      # check if switch pressed
        # If so shift to using the Amazon Kinesis service
            while (1):
                # current mode of operation
                myLcd.clear()        # clear
                myLcd.setCursor(0,0) # zero the cursor
                myLcd.write("Using Amazon Kinesis...")

                # Read temperature here in celsius
                temp = tempSensor.read()
                # ADC has output range 0 to 1023
                # Temp sensor works from -40C to 125C,
                # 165 degree range ofset by 40 degrees C
                R = 1023.0/temp - 1.0
                R = 100000.0*R
                # thermister B=4275
                c = 1.0/(math.log10(R/100000.0)/4275+1/298.15)-273.15

                # number of readings: n

                # timestamp of reading: t

                # Convert to F
                f = c * 9.0/5.0 + 32.0;
                # Print it in the console
                print "%d degrees C, or %d degrees F" \
                % (celsius, fahrenheit)
                # Post to Kinesis

                if (switch.read()):      # check if switch pressed
                    return


except KeyboardInterrupt:
    exit
except:
    print "Error"
    return False
