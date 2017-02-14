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
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
from boto import kinesis
from datetime import datetime
import pyupm_i2clcd as lcd
import json
import time
import mraa
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

# Prepare Kinesis client
client_kinesis = boto.connect_kinesis(
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)
KINESIS_STREAM_NAME = 'temp_stream'

# Initialize variables
a = 0
i = 1
j = 1

# Delete a DynamoDB table.
def delete_table(name):
    # input must be string
    try:
        table = Table(name, connection=client_dynamo)
        table.delete()
        print 'waiting for deletion...'
        time.sleep(12)
        return
    except KeyboardInterrupt:
        exit
    except:
        print "Error in delete_table()"
        return False

# Create the DynamoDB table.
def create_table(name,hashkey,rangekey):
    try:
        table = Table.create(name, schema=[HashKey(hashkey),RangeKey(rangekey)], connection=client_dynamo)
        print 'writing...'
        time.sleep(12)
        return True
    except KeyboardInterrupt:
        exit
    except:
        print "Error in create_table()"
        return False

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
    except:
        print "Error in create_item()"
        return False

# delete old table and create new one if (no old then error)
delete_table('temp_stream')
create_table('temp_stream','measurement-iteration','temp')

print "Press Ctrl+C to escape..."
try:
    while (1):
        if (switch.read()):
            a = a+1
            time.sleep(0.25)
        if  a%2==0:
            # current mode of operation
            myLcd.clear()        # clear
            myLcd.setCursor(0,0) # zero the cursor
            myLcd.write("DynamoDB")
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
            celsius = 1.0/(math.log10(R/100000.0)/4275+1/298.15)-273.15
            # Convert to F
            fahrenheit = celsius * 9.0/5.0 + 32.0;
            # Get current time
            current_time = str(datetime.now())
            # Print it in the console
            print "%d , %d degrees C, %d degrees F, %s o'clock" \
            % (i, celsius, fahrenheit, current_time)
            # Post temperature to DynamoDB
            d = {
                'measurement-iteration': '%d'%i,
                'temp': '%s'%celsius,
                'timestamp': '%s'%current_time,
            }
            create_item('temp_stream', d)
            i =  i + 1
            time.sleep(0.1)

        if  a%2==1:
            # current mode of operation
            myLcd.clear()        # clear
            myLcd.setCursor(0,0) # zero the cursor
            myLcd.write("Kinesis Stream")

            # Read temperature here in celsius
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
            # Get current time
            current_time = str(datetime.now())
            # Print it in the console
            print "%d , %d degrees C, %d degrees F, %s o'clock" \
            % (i, celsius, fahrenheit, current_time)
            # Post to Kinesis
            package = (j,celsius,current_time)
            client_kinesis.put_record(KINESIS_STREAM_NAME, json.dumps(package), "partitionkey")
            j =  j + 1
            time.sleep(0.1)

except KeyboardInterrupt:
    exit
except:
    print "Error: Main Loop"
