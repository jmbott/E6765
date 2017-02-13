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
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from boto import kinesis
import mraa
import time
import pyupm_i2clcd as lcd
from datetime import datetime
import math
import json

tempSensor = mraa.Aio(1)
switch_pin_number=8
# Configuring the switch as GPIO interfaces
switch = mraa.Gpio(switch_pin_number)
# Configuring the switch as an input
switch.dir(mraa.DIR_IN)

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Yellow LCD
myLcd.setColor(255, 255, 0)

ACCOUNT_ID = '485969833300'
IDENTITY_POOL_ID = 'us-east-1:00ca87ab-bb9e-4736-a526-9f077b3990c8'
ROLE_ARN = 'arn:aws:iam::485969833300:role/Cognito_edisonDemoKinesisUnauth_Role'
# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])

# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

DYNAMODB_TABLE_NAME = 'edisonDemoDynamo'

# Prepare DynamoDB client
client_dynamo = boto.dynamodb2.connect_to_region(
            'us-east-1',
            aws_access_key_id=assumedRoleObject.credentials.access_key,
            aws_secret_access_key=assumedRoleObject.credentials.secret_key,
            security_token=assumedRoleObject.credentials.session_token)


KINESIS_STREAM_NAME = 'edisonDemoKinesis'
table_dynamo = Table("temp", connection=client_dynamo)
# Prepare Kinesis client
client_kinesis = boto.connect_kinesis(
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)
a = 0    
i = 1
j = 1
print "Press Ctrl+C to escape..."
try:
    while (1):
        if (switch.read()):
            a = a+1
            time.sleep(0.25)
        if  a%2==0:  
            myLcd.clear()        # clear
            myLcd.setCursor(0,0) # zero the cursor
            myLcd.write("DynamoDB")
            temp = tempSensor.read()
            R = 1023.0/temp - 1.0
            R = 100000.0*R
            celsius = 1.0/(math.log10(R/100000.0)/4275+1/298.15)-273.15
            current_time = str(datetime.now()) 
            table_dynamo.put_item({
                'temp': '%s'%celsius,
                'timestamp': '%s'%current_time,
                'measurement-iteration': '%d'%i,
            })
            
            i =  i + 1
            time.sleep(0.1)
            
        if  a%2==1:  
            myLcd.clear()        # clear
            myLcd.setCursor(0,0) # zero the cursor
            myLcd.write("Kinesis Stream")
            temp = tempSensor.read()
            R = 1023.0/temp - 1.0
            R = 100000.0*R
            celsius = 1.0/(math.log10(R/100000.0)/4275+1/298.15)-273.15
            current_time = str(datetime.now())
            package = (j,celsius,current_time)
            j =  j + 1
            client_kinesis.put_record(KINESIS_STREAM_NAME, json.dumps(package), "partitionkey")
            time.sleep(0.1)
                      
except KeyboardInterrupt:
    exit
