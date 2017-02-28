#
# IOT E6756 Lab Assignment 4
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# Question 2 (80 pts)
# This week's exercise builds on what you have developed last week. Do run your
# solution to Assignment 3 to populate your table. Alternately, incorporate
# that code into your solution for this week. There are no points for either
# approach.
#
# Your source station is 116th Street, Columbia University (Station ID: 117S).
# Destination station is 42nd Street, Times Square (Station ID: 127S).
#
# You must create an interactive menu this week with 3 options.
# >> Plan trip: (Generate a notification on whether to "Switch" or "Stay" at
# the 96th Station)
# >> Subscribe to message feed: (Ask the user for his/her phone number & send
# a subscription message to the same)
# >> Exit (Exit and close program)
#
# 1. (10 pts) Get a list of local trains (ie, 1 trains) passing through the
# 96th station
# 2. (10 pts) Repeat the same for express trains (ie, 2 or 3 trains)
# 3. (10 pts) After you reach 96th from your source station find & display
# tripId of earliest local train reaching the 96th station.
# 4. (10 pts) Repeat 3. for express trains.
# 5. (10 pts) Print time taken to reach 42nd in each case. ("time" = time from
# source station to destination station)
# 6. (10 pts) Print whether user should "Switch to Express Train" or "Stay on
# in the Local Train", and send this to all your subscribers.
# 7. (10 pts) Error Handling
# 8. (10 pts)Generalize such that you could select any source station (on the
# local 1 train line) North of the 96th Street stop while heading downtown.
# Additionally, allow for a journey uptown from 42nd Street to any stop North
# of 96th Street. Essentially, you will choose whether or not to get on the
# express at 42nd Street. If you choose to get on the express, you will have
# to get off at 96th Street.
#
# Stations:
# 242nd St (1) = 101
# 238th St (1) = 103
# 231th St (1) = 104
# 225th St (1) = 106
# 215th St (1) = 107
# 207nd St (1) = 108
# Dyckman St (1) = 109
# 191st St (1) = 110
# 181st St (1) = 111
# 168th St (1) = 112
# 157th St (1) = 113
# 145th St (1) = 114
# 137th St (1) = 115
# 125th St (1) = 116
# 116th St (1) = 117
# 110th St (1) = 118
# 96th St (1,2,3) = 120
# 86th St (1) = 121
# 79th St (1) = 122
# 72nd St (1,2,3) = 123
# 66th St (1) = 124
# 59th St (1) = 125
# 50th St (1) = 126
# 42nd St (1,2,3) = 127
#

import time

import boto3
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError

from utils import aws

# Get the service resource.
def get_resource():
    try:
        global dynamodb, table
        dynamodb = aws.getResource('dynamodb', 'us-east-1')
        table = dynamodb.Table("mtaData")
    except KeyboardInterrupt:
        exit
    except:
        print "Get Resource Failure"

# Get a list of local or express trains passing through the 96th station
def list_trains(speed):
    try:
        m = []
        if speed == 'local':
            response = table.scan(
                FilterExpression=Attr('routeId').eq('1')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find('120N')
                y = out.find('120S')
                if x != -1:
                    m.append(n['tripId'])
                if y != -1:
                    m.append(n['tripId'])
        elif speed == 'express':
            response = table.scan(
                FilterExpression=Attr('routeId').eq('2')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find('120N')
                y = out.find('120S')
                if x != -1:
                    m.append(n['tripId'])
                if y != -1:
                    m.append(n['tripId'])
            response = table.scan(
                FilterExpression=Attr('routeId').eq('3')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find('120N')
                y = out.find('120S')
                if x != -1:
                    m.append(n['tripId'])
                if y != -1:
                    m.append(n['tripId'])
        else:
            return False
        return m
    except KeyboardInterrupt:
        exit
    except ClientError:
        get_resource()
        print "Token Updated, Retry"
    except:
        print "Error listing trains"

# Find and display tripId of earliest train reaching the 96th street station
# after a designated time t_delta (for travel time to 96th)
#
#  t_arrival    t_delta    t_current
#      |<--------------------->|
#
def list_earliest(speed, direction, t_delta=0):
    try:
        t_arrival = 9999999999
        i = None
        if t_delta < 0:
            print "t_delta must be greater than or equal to zero"
            return False
        if direction == 'north':
            d = 'N'
        elif direction == 'south':
            d = 'S'
        else:
            print "Improper direction"
            return False
        if speed == 'local':
            response = table.scan(
                FilterExpression=Attr('routeId').eq('1')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find('120' + d)
                if x != -1:
                    t_new = int(out[x-23:x-13])
                    t_current = n['ts']
                    if t_current + t_delta <= t_new and t_arrival > t_new:
                        t_arrival = t_new
                        i = n['tripId']
        if speed == 'express':
            response = table.scan(
                FilterExpression=Attr('routeId').eq('2')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find('120' + d)
                if x != -1:
                    t_new = int(out[x-23:x-13])
                    t_current = n['ts']
                    if t_current + t_delta <= t_new and t_arrival > t_new:
                        t_arrival = t_new
                        i = n['tripId']
            response = table.scan(
                FilterExpression=Attr('routeId').eq('3')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find('120' + d)
                if x != -1:
                    t_new = int(out[x-23:x-13])
                    t_current = n['ts']
                    if t_current + t_delta <= t_new and t_arrival > t_new:
                        t_arrival = t_new
                        i = n['tripId']
        return {'tripId':i, 'time':t_arrival}
    except KeyboardInterrupt:
            exit
    except ClientError:
        get_resource()
        print "Token Updated, Retry"
    except:
        print "Error listing earliest train"

# Print time taken to reach destination station on a local or express train
# from source station. The options are below:
def time_to(speed, source, destination, t_delta=0):
    try:
        t = 9999999999
        t_2 = t_3 = t
        if t_delta < 0:
            print "t_delta must be greater than or equal to zero"
            return False
        if int(destination) > int(source):
            direction = 'S'
        elif int(destination) < int(source):
            direction = 'N'
        else:
            print "destination and source are the same"
            return False
        if speed == 'local':
            response = table.scan(
                FilterExpression=Attr('routeId').eq('1')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find(str(source) + direction)
                if x != -1:
                    y = out.find(str(destination) + direction)
                    if y != -1:
                        t_source = int(out[x-23:x-13])
                        t_destination = int(out[y-23:y-13])
                        t_new = t_destination - t_source
                        t_current = n['ts']
                        if t_current + t_delta <= t_source and t > t_new:
                            t = t_new
        if speed == 'express':
            if str(source) != '120' and str(source) != '123' and str(source) != '127':
                print "not an express source"
                return False
            if str(destination)!='120' and str(destination)!='123' and str(destination)!='127':
                print "not an express destination"
                return False
            response = table.scan(
                FilterExpression=Attr('routeId').eq('2')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find(str(source) + direction)
                if x != -1:
                    y = out.find(str(destination) + direction)
                    if y != -1:
                        t_source = int(out[x-23:x-13])
                        t_destination = int(out[y-23:y-13])
                        t_new = t_destination - t_source
                        t_current = n['ts']
                        if t_current + t_delta <= t_source and t_2 > t_new:
                            t_2 = t_new
            response = table.scan(
                FilterExpression=Attr('routeId').eq('3')
            )
            items = response['Items']
            for n in items:
                out = n['futureStopData']
                x = out.find(str(source) + direction)
                if x != -1:
                    y = out.find(str(destination) + direction)
                    if y != -1:
                        t_source = int(out[x-23:x-13])
                        t_destination = int(out[y-23:y-13])
                        t_new = t_destination - t_source
                        t_current = n['ts']
                        if t_current + t_delta <= t_source and t_3 > t_new:
                            t_3 = t_new
            if t_2 < t_3:
                t = t_2
            elif t_3 < t_2:
                t = t_3
            else:
                t = t_2
        return t
    except KeyboardInterrupt:
        exit
    except ClientError:
        get_resource()
        print "Token Updated, Retry"
    except:
        print "Error getting time to"

def choose(destination,t_d1,station):
    try:
        t_d2l = time_to('local', str(station), str(destination), t_d1)
        t_d2e = time_to('express', str(station), str(destination), t_d1)
        if t_d2l < t_d2e:
            decision = "Stay on in the Local Train"
        elif t_d2l > t_d2e:
            decision = "Switch to Express Train"
        else:
            decision = "Tie, Stay on in the Local Train"
        return decision
    except KeyboardInterrupt:
        exit
    except:
        print "Error in choose"

# Flexible decision whether or not to switch at 96th st
def switch_decision(source,destination):
    try:
        if int(destination) > int(source):
            direction = 'S'
        elif int(destination) < int(source):
            direction = 'N'
        else:
            print "destination and source are the same"
            return False
        if int(source) < 120 and direction == 'S' and int(destination) >= 123:
            t_d1 = time_to('local', source, '120')
            decision = choose(destination,t_d1,'120')
        elif int(source) == 120 and direction == 'S' and int(destination) >= 123:
            decision = choose(destination,0,'120')
        elif int(source) < 123 and direction == 'S' and int(destination) >= 127:
            t_d1 = time_to('local', source, '123')
            decision = choose(destination,t_d1,'123')
        elif int(source) == 123 and direction == 'S' and int(destination) >= 127:
            decision = choose(destination,0,'123')
        elif int(source) <= 127 and direction == 'S' and int(destination) > 127:
            decision = "Out of Range"
        elif int(source) > 127 and direction == 'N':
            decision = "Out of Range"
        elif int(source) == 127 and direction == 'N' and int(destination) <= 123:
            decision = choose(destination,0,'127')
        elif int(source) > 123 and direction == 'N' and int(destination) <= 120:
            t_d1 = time_to('local', source, '123')
            decision = choose(destination,t_d1,'123')
        elif int(source) == 123 and direction == 'N' and int(destination) <= 120:
            decision = choose(destination,0,'123')
        else:
            decision = "Stay on in the Local Train"
        return decision
    except KeyboardInterrupt:
        exit
    except ClientError:
        get_resource()
        print "Token Updated, Retry"
    except:
        print "Error in switch decision"

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

menu = {}
menu['1']="List trains passing 96th going south from 116th"
menu['2']="List tripId of earliest train at 96th going south from 116th"
menu['3']="Time to reach 42nd going south from 116th"
menu['4']="Send trip decision to SNS subscribers"
menu['5']="Print switch decision"
menu['6']="Exit"

print "Press Ctrl+C to escape..."
try:
    while True:
        get_resource()
        options=menu.keys()
        options.sort()
        for entry in options:
            print entry, menu[entry]
        selection=raw_input("Please Select:")
        print ""
        # list trains passing 96th
        if selection =='1':
            speed=raw_input("List local or express trains?")
            print ""
            list_trains(speed)
            print ""
        # Find and display tripId of earliest train reaching the 96th station
        elif selection == '2':
            speed=raw_input("On local or express train?")
            print ""
            direction=raw_input("Going north or south?")
            print ""
            list_earliest(speed, direction, t_delta=0)
            print ""
        # Print time taken to reach 42nd for local or express train
        elif selection == '3':
            speed=raw_input("On local or express train?")
            print ""
            source=raw_input("From what station?")
            time_to(speed, source, '127', t_delta=0)
            print ""
        # "Switch to Express Train" or "Stay on in the Local Train"
        # Send to SNS subscribers
        elif selection == '4':
            source=raw_input("From what station?")
            print ""
            destination=raw_input("To what station?")
            print ""
            decision = switch_decision(source,destination)
            if destination == "Stay on in the Local Train":
                print "Stay on in the Local Train"
                publish("Train Choice","Stay on in the Local Train")
            elif destination == "Switch to Express Train":
                print "Switch to Express Train"
                publish("Train Choice","Switch to Express Train")
            elif destination == "Tie, Stay on in the Local Train":
                print "Tie, Stay on in the Local Train"
                publish("Train Choice","Tie, Stay on in the Local Train")
            else:
                print "Out of Range"
                publish("Train Choice","Out of Range")
            print ""
        # Flexible decision whether or not to switch trains
        elif selection == '5':
            source=raw_input("From what station?")
            print ""
            destination=raw_input("To what station?")
            print ""
            switch_decision(source,destination)
            print ""
        # exit
        elif selection == '6':
            break
        else:
            print "Unknown Option Selected!"
            print ""
except KeyboardInterrupt:
        exit
except:
    print "Error in Main Loop"


# Deal with it if there is nothing in the database
# Deal with it if there is not a database
