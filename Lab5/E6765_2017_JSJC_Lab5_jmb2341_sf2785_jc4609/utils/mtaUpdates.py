import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
from protos import gtfs_realtime_pb2
import google.protobuf
import sys
import time
import datetime
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
        self.D['ts'] = 'None'
        self.D['tripId'] = 'None'
        self.D['routeId'] = 'None'
        self.D['dow'] = 'None'
        self.D['96_arrive'] = 'None'
        self.D['42_arrive'] = 'None'
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
        try:
            dynamodb = aws.getResource('dynamodb', 'us-east-1')
            table = dynamodb.Table("mtadata5")
            for entity in feed.entity:
                #try:
                if entity.HasField('vehicle'):
                    mark_96 = 0
                    mark_42 = 0
                    write = 0
                    # timeStamp: Feed timestamp [EDIT: This timestamp can be
                    #  obtained from the mta feed's header message]
                    ts = feed.header.timestamp
                    # Unix time is # of seconds since January 1, 1970 00:00 UTC
                    hour = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%H')) - 5
                    minute = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%M'))
                    # Timestamp in minutes past midnight
                    m = hour*60 + minute
                    self.D['ts'] = m
                    # day of the week
                    today = date.fromtimestamp(ts)
                    dow = date.weekday(today)
                    if dow == 6 or dow == 7:
                        dow = "weekend"
                    else:
                        dow = "weekday"
                    self.D['dow'] = dow
                    e = entity
                    # tripId: The unique trip identifier
                    tripid = e.vehicle.trip.trip_id
                    # tripId: Constructed from the scheduled start time of the trip and a shape_id:
                    # <start time>_<shape_id>. The start time is represented as hundredths of
                    # minutes past midnight, six digits 0 padded. So, 6:45:30am would be
                    # 040550.
                    # minutes past midnight
                    self.num = tripid[7:8]
                    if self.num != '1' and self.num != '2' and self.num != '3':
                        write = 1
                    self.D['tripId'] = str(float(tripid[0:6])*0.01)
                    # Time at which it reaches express station (at 96th street)
                    # taken from the "vehicle message" of the MTA feed when possible
                    # alt from "arrival time" from the 'trip_update' message
                    current_stop = e.vehicle.stop_id
                    if current_stop == "120S":
                        ts = e.vehicle.timestamp
                        hour = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%H')) - 5
                        minute = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%M'))
                        m = hour*60 + minute
                        mark_96 = 1
                        self.D['96_arrive'] = m
                    # Time at which it reaches the destination (at 42nd Street)
                    # taken from the "vehicle message" of the MTA feed when possible
                    # alt from "arrival time" from the 'trip_update' message
                    if current_stop == "127S":
                        ts = e.vehicle.timestamp
                        hour = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%H')) - 5
                        minute = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%M'))
                        m = hour*60 + minute
                        mark_42 = 1
                        self.D['42_arrive'] = m
                    if write == 1:
                        pass
                    elif mark_42 == 1:
                        # Post dict
                        try:
                            table.update_item(
                                Key={
                                    'tripId':self.D['tripId']
                                },
                                UpdateExpression=
                                    "set ts =:a,dow=:b,96_arrive=:c",
                                ExpressionAttributeValues={
                                    ':a':self.D['ts'],
                                    ':b':self.D['dow'],
                                    ':c':self.D['96_arrive']
                                }
                            )
                        except KeyboardInterrupt:
                            exit
                        except:
                            print "Update Error 1"
                    elif mark_96 == 1:
                        # Post dict
                        try:
                            table.update_item(
                                Key={
                                    'tripId':self.D['tripId']
                                },
                                UpdateExpression=
                                    "set ts =:a,dow=:b,42_arrive=:c",
                                ExpressionAttributeValues={
                                    ':a':self.D['ts'],
                                    ':b':self.D['dow'],
                                    ':c':self.D['42_arrive']
                                }
                            )
                        except KeyboardInterrupt:
                            exit
                        except:
                            print "Update Error 2"
                    else:
                        # Post dict
                        try:
                            table.update_item(
                                Key={
                                    'tripId':self.D['tripId']
                                },
                                UpdateExpression=
                                    "set ts = :a,dow=:b",
                                ExpressionAttributeValues={
                                    ':a':self.D['ts'],
                                    ':b':self.D['dow']
                                }
                            )
                        except KeyboardInterrupt:
                            exit
                        except:
                            print "Update Error 3"
                if entity.HasField('trip_update'):
                    mark_96 = 0
                    mark_42 = 0
                    write = 0
                    # timeStamp: Feed timestamp [EDIT: This timestamp can be
                    #  obtained from the mta feed's header message]
                    ts = feed.header.timestamp
                    # Unix time is # of seconds since January 1, 1970 00:00 UTC
                    hour = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%H')) - 5
                    minute = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%M'))
                    # Timestamp in minutes past midnight
                    m = hour*60 + minute
                    self.D['ts'] = m
                    # day of the week
                    today = date.fromtimestamp(ts)
                    dow = date.weekday(today)
                    if dow == 6 or dow == 7:
                        dow = "weekend"
                    else:
                        dow = "weekday"
                    self.D['dow'] = dow
                    e = entity
                    # tripId: The unique trip identifier
                    tripid = e.trip_update.trip.trip_id
                    # tripId: Constructed from the scheduled start time of the trip and a shape_id:
                    # <start time>_<shape_id>. The start time is represented as hundredths of
                    # minutes past midnight, six digits 0 padded. So, 6:45:30am would be
                    # 040550.
                    # minutes past midnight
                    self.D['tripId'] = str(float(tripid[0:6])*0.01)
                    # routeId: Train Route, eg, 1, 2, 3 etc. or "S" for the Grand
                    #  Shuttle Service between Times Square & Grand Central
                    self.D['routeId'] = e.trip_update.trip.route_id
                    if self.D['routeId'] != '1' and self.D['routeId'] != '2' and self.D['routeId'] != '3':
                        write = 1
                    # Message feed, regarding the message itself.
                    # futureStopData: Information from the trip_update message.
                    #  Should contain:
                    #  {<stop_id>: ["arrivaltime": <arrival_at_stop>, "departuretime": <departure_from_stop>]}
                    #  for eg.
                    #  {"247N": [{"arrivalTime":1454802090}, {"departureTime": 1454802090}], "246N": [{"arrivalTime": 1454802210}, {"departureTime": 1454802210}]}
                    out = str(e.trip_update.stop_time_update)
                    z = out.find('stop_id')
                    x = out.find('120S')
                    y = out.find('127S')
                    if z != -1:
                        i = out[z+10:z+14]
                        if i == '120S':
                            mark_96 = 1
                        elif i == '127S':
                            mark_42 = 1
                        elif y == -1:
                            mark_42 = 1
                        elif x == -1:
                            mark_96 = 1
                    # Time at which it reaches the destination
                    # taken from the "vehicle message" of the MTA feed when possible
                    # alt from "arrival time" from the 'trip_update' message
                    self.D['42_arrive'] = out[y-29:y-19]
                    self.D['96_arrive'] = out[x-29:x-19]
                    if write == 1:
                        pass
                    elif mark_42 == 1:
                        # Post dict
                        try:
                            table.update_item(
                                Key={
                                    'tripId':self.D['tripId']
                                },
                                UpdateExpression=
                                    "set ts = :a,dow=:b,routeId=:c",
                                ExpressionAttributeValues={
                                    ':a':self.D['ts'],
                                    ':b':self.D['dow'],
                                    ':c':self.D['routeId']
                                }
                            )
                        except KeyboardInterrupt:
                            exit
                        except:
                            print "Update Error 4"
                    elif mark_96 == 1:
                        # Post dict
                        try:
                            table.update_item(
                                Key={
                                    'tripId':self.D['tripId']
                                },
                                UpdateExpression=
                                    "set ts = :a,dow=:b,routeId=:c,42_arrive=:d",
                                ExpressionAttributeValues={
                                    ':a':self.D['ts'],
                                    ':b':self.D['dow'],
                                    ':c':self.D['routeId'],
                                    ':d':self.D['42_arrive']
                                }
                            )
                        except KeyboardInterrupt:
                            exit
                        except:
                            print "Update Error 5"
                    else:
                        # Post dict
                        try:
                            table.update_item(
                                Key={
                                    'tripId':self.D['tripId']
                                },
                                UpdateExpression=
                                    "set ts = :a,dow=:b,routeId=:c,42_arrive=:d,96_arrive=:e",
                                ExpressionAttributeValues={
                                    ':a':self.D['ts'],
                                    ':b':self.D['dow'],
                                    ':c':self.D['routeId'],
                                    ':d':self.D['42_arrive'],
                                    ':e':self.D['96_arrive']
                                }
                            )
                        except KeyboardInterrupt:
                            exit
                        except:
                            print "Update Error 6"
            #except KeyboardInterrupt:
            #    exit
            #except:
            #    print "For Loop Error 1"

        except KeyboardInterrupt:
            exit
        except:
            print "mtaUpdates Error"
