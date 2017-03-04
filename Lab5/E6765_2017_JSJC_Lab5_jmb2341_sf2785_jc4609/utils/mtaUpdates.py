import urllib2,contextlib
from collections import OrderedDict

from pytz import timezone
from protos import gtfs_realtime_pb2
import google.protobuf
import sys
import time
from datetime import date, datetime

import boto3
from boto3.dynamodb.conditions import Key,Attr
from utils import aws

class mtaUpdates:
    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')
    # Note that Feed_ID=1 applies to the 1,2,3,4,5,6 & Grand Central Shuttle
    MTA_FEED = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='
    # Reading from the key file (you may need to change file path).
    with open('./utils/key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()
    def __init__(self, FEED=1):
        self.FEED = str(FEED)
        self.FEED_URL = self.MTA_FEED + self.APIKEY
        self.D = OrderedDict()
    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        ## Using the gtfs_realtime_pb2 file created by the
        ## proto compiler, we view the feed using the method below.
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            with contextlib.closing(urllib2.urlopen(self.FEED_URL)) as response:
                d = feed.ParseFromString(response.read())
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " +str(e)
        ########################################################################
        ####### Run code above this point to validate your connection ##########
        ########################################################################
        ## The MTA feed gives entities which give information regarding,
        ## vehicle status, trip_update information & alerts
        self.timestamp = feed.header.timestamp
        self.nytime = datetime.fromtimestamp(self.timestamp,self.TIMEZONE)
        #try:
        dynamodb = aws.getResource('dynamodb', 'us-east-1')
        table = dynamodb.Table("mtadata5")
        for entity in feed.entity:
            #try:
            if entity.HasField('vehicle'):
                self.mark_96 = 0
                self.mark_42 = 0
                self.write = 0
                # timeStamp: Feed timestamp [EDIT: This timestamp can be
                #  obtained from the mta feed's header message]
                self.ts = int(feed.header.timestamp) - 18000
                # Unix time is # of seconds since January 1, 1970 00:00 UTC
                self.hour = int(datetime.fromtimestamp(int(self.ts)).strftime('%H'))
                self.minute = int(datetime.fromtimestamp(int(self.ts)).strftime('%M'))
                # Timestamp in minutes past midnight
                self.m = self.hour*60 + self.minute
                self.D['ts'] = self.m
                # day of the week
                self.today = date.fromtimestamp(self.ts)
                self.dow = date.weekday(self.today)
                if self.dow == 5 or self.dow == 6:
                    self.dow = "weekend"
                else:
                    self.dow = "weekday"
                self.D['dow'] = self.dow
                e = entity
                # tripId: The unique trip identifier
                self.tripid = e.vehicle.trip.trip_id
                # tripId: Constructed from the scheduled start time of the trip and a shape_id:
                # <start time>_<shape_id>. The start time is represented as hundredths of
                # minutes past midnight, six digits 0 padded. So, 6:45:30am would be
                # 040550.
                # minutes past midnight
                self.num = self.tripid[7:8]
                if self.num != '1' and self.num != '2' and self.num != '3':
                    self.write = 1
                self.D['tripId'] = str(float(self.tripid[0:6])*0.01)
                # Time at which it reaches express station (at 96th street)
                # taken from the "vehicle message" of the MTA feed when possible
                # alt from "arrival time" from the 'trip_update' message
                self.current_stop = e.vehicle.stop_id
                if self.current_stop == "120S":
                    self.ts = int(e.vehicle.timestamp) - 18000
                    self.hour = int(datetime.fromtimestamp(int(self.ts)).strftime('%H'))
                    self.minute = int(datetime.fromtimestamp(int(self.ts)).strftime('%M'))
                    self.m = self.hour*60 + self.minute
                    self.mark_96 = 1
                    self.D['96_arrive'] = str(self.m)
                # Time at which it reaches the destination (at 42nd Street)
                # taken from the "vehicle message" of the MTA feed when possible
                # alt from "arrival time" from the 'trip_update' message
                elif self.current_stop == "127S":
                    self.ts = int(e.vehicle.timestamp) - 18000
                    self.hour = int(datetime.fromtimestamp(int(self.ts)).strftime('%H'))
                    self.minute = int(datetime.fromtimestamp(int(self.ts)).strftime('%M'))
                    self.m = self.hour*60 + self.minute
                    self.mark_42 = 1
                    self.D['42_arrive'] = str(self.m)
                else:
                    self.write = 1
                # direction: "N" or "S" depending on whether the journey is
                # uptown or downtown, respectively.
                self.direction = self.tripid[10:11]
                if self.direction == 'N':
                    self.write = 1
                if self.write == 1:
                    pass
                elif self.mark_42 == 1:
                    # Post dict
                    #try:
                    table.update_item(
                        Key={
                            'tripId':self.D['tripId']
                        },
                        UpdateExpression=
                            "set ts=:a,dow=:b,TimesSquareArrive=:c",
                        ExpressionAttributeValues={
                            ':a':self.D['ts'],
                            ':b':self.D['dow'],
                            ':c':self.D['42_arrive']
                        }
                    )
                    #except KeyboardInterrupt:
                    #    exit
                    #except:
                    #    print "Update Error 1"
                elif self.mark_96 == 1:
                    # Post dict
                    #try:
                    table.update_item(
                        Key={
                            'tripId':self.D['tripId']
                        },
                        UpdateExpression=
                            "set ts=:a,dow=:b,NinetySixArrive=:c",
                        ExpressionAttributeValues={
                            ':a':self.D['ts'],
                            ':b':self.D['dow'],
                            ':c':self.D['96_arrive']
                        }
                    )
                    #except KeyboardInterrupt:
                    #    exit
                    #except:
                    #    print "Update Error 2"
                else:
                    # Post dict
                    #try:
                    table.update_item(
                        Key={
                            'tripId':self.D['tripId']
                        },
                        UpdateExpression=
                            "set ts=:a,dow=:b",
                        ExpressionAttributeValues={
                            ':a':self.D['ts'],
                            ':b':self.D['dow']
                        }
                    )
                    #except KeyboardInterrupt:
                    #    exit
                    #except:
                    #    print "Update Error 3"
            if entity.HasField('trip_update'):
                self.mark_96 = 0
                self.mark_42 = 0
                self.write = 0
                # timeStamp: Feed timestamp [EDIT: This timestamp can be
                #  obtained from the mta feed's header message]
                self.ts = int(feed.header.timestamp) - 18000
                # Unix time is # of seconds since January 1, 1970 00:00 UTC
                self.hour = int(datetime.fromtimestamp(int(self.ts)).strftime('%H'))
                self.minute = int(datetime.fromtimestamp(int(self.ts)).strftime('%M'))
                # Timestamp in minutes past midnight
                self.m = self.hour*60 + self.minute
                self.D['ts'] = self.m
                # day of the week
                self.today = date.fromtimestamp(self.ts)
                self.dow = date.weekday(self.today)
                if self.dow == 5 or self.dow == 6:
                    self.dow = "weekend"
                else:
                    self.dow = "weekday"
                self.D['dow'] = self.dow
                e = entity
                # tripId: The unique trip identifier
                self.tripid = e.trip_update.trip.trip_id
                # tripId: Constructed from the scheduled start time of the trip and a shape_id:
                # <start time>_<shape_id>. The start time is represented as hundredths of
                # minutes past midnight, six digits 0 padded. So, 6:45:30am would be
                # 040550.
                # minutes past midnight
                self.D['tripId'] = str(float(self.tripid[0:6])*0.01)
                # routeId: Train Route, eg, 1, 2, 3 etc. or "S" for the Grand
                #  Shuttle Service between Times Square & Grand Central
                self.D['routeId'] = e.trip_update.trip.route_id
                if self.D['routeId'] != '1' and self.D['routeId'] != '2' and self.D['routeId'] != '3':
                    self.write = 1
                # Message feed, regarding the message itself.
                # futureStopData: Information from the trip_update message.
                #  Should contain:
                #  {<stop_id>: ["arrivaltime": <arrival_at_stop>, "departuretime": <departure_from_stop>]}
                #  for eg.
                #  {"247N": [{"arrivalTime":1454802090}, {"departureTime": 1454802090}], "246N": [{"arrivalTime": 1454802210}, {"departureTime": 1454802210}]}
                self.out = str(e.trip_update.stop_time_update)
                self.z = self.out.find('stop_id')
                self.x = self.out.find('120S')
                self.y = self.out.find('127S')
                if self.z != -1:
                    self.i = self.out[self.z+10:self.z+14]
                    if self.i == '120S':
                        self.mark_96 = 1
                    elif self.i == '127S':
                        self.mark_42 = 1
                    elif self.y == -1:
                        self.write = 1
                    elif self.x == -1:
                        self.mark_96 = 1
                else:
                    print "error, no stop_id"
                # direction: "N" or "S" depending on whether the journey is
                # uptown or downtown, respectively.
                self.direction = e.trip_update.trip.trip_id[10:11]
                if self.direction == 'N':
                    self.write = 1
                # Time at which it reaches the destination
                # taken from the "vehicle message" of the MTA feed when possible
                # alt from "arrival time" from the 'trip_update' message
                if self.mark_96 == 1:
                    self.ts = int(self.out[self.y-23:self.y-13]) - 18000
                    self.hour = int(datetime.fromtimestamp(int(self.ts)).strftime('%H'))
                    self.minute = int(datetime.fromtimestamp(int(self.ts)).strftime('%M'))
                    self.m = self.hour*60 + self.minute
                    self.D['42_arrive'] = str(self.m)
                elif self.mark_42 == 1:
                    pass
                elif self.write == 0:
                    self.ts = int(self.out[self.y-23:self.y-13]) - 18000
                    self.hour = int(datetime.fromtimestamp(int(self.ts)).strftime('%H'))
                    self.minute = int(datetime.fromtimestamp(int(self.ts)).strftime('%M'))
                    self.m = self.hour*60 + self.minute
                    self.D['42_arrive'] = str(self.m)
                    self.ts = int(self.out[self.x-23:self.x-13]) - 18000
                    self.hour = int(datetime.fromtimestamp(int(self.ts)).strftime('%H'))
                    self.minute = int(datetime.fromtimestamp(int(self.ts)).strftime('%M'))
                    self.m = self.hour*60 + self.minute
                    self.D['96_arrive'] = str(self.m)

                self.D['futureStopData'] = str(e.trip_update.stop_time_update)

                if self.write == 1:
                    pass
                elif self.mark_42 == 1:
                    # Post dict
                    #try:
                    table.update_item(
                        Key={
                            'tripId':self.D['tripId']
                        },
                        UpdateExpression=
                            "set ts=:a,dow=:b,routeId=:c",
                        ExpressionAttributeValues={
                            ':a':self.D['ts'],
                            ':b':self.D['dow'],
                            ':c':self.D['routeId']
                        }
                    )
                    #except KeyboardInterrupt:
                    #    exit
                    #except:
                    #    print "Update Error 4"
                elif self.mark_96 == 1:
                    # Post dict
                    #try:
                    table.update_item(
                        Key={
                            'tripId':self.D['tripId']
                        },
                        UpdateExpression=
                            "set ts=:a,dow=:b,routeId=:c,TimesSquareArrive=:d",
                        ExpressionAttributeValues={
                            ':a':self.D['ts'],
                            ':b':self.D['dow'],
                            ':c':self.D['routeId'],
                            ':d':self.D['42_arrive']
                        }
                    )
                    #except KeyboardInterrupt:
                    #    exit
                    #except:
                    #    print "Update Error 5"
                else:
                    # Post dict
                    #try:
                    table.update_item(
                        Key={
                            'tripId':self.D['tripId']
                        },
                        UpdateExpression=
                            "set ts=:a,dow=:b,routeId=:c,TimesSquareArrive=:d,NinetySixArrive=:e",
                        ExpressionAttributeValues={
                            ':a':self.D['ts'],
                            ':b':self.D['dow'],
                            ':c':self.D['routeId'],
                            ':d':self.D['42_arrive'],
                            ':e':self.D['96_arrive']
                        }
                    )
                    #except KeyboardInterrupt:
                    #    exit
                    #except:
                    #    print "Update Error 6"
        #except KeyboardInterrupt:
        #    exit
        #except:
        #    print "For Loop Error 1"

    #except KeyboardInterrupt:
    #    exit
    #except:
    #    print "mtaUpdates Error"
