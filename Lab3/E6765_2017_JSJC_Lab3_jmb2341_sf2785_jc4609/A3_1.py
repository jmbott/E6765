#
# IOT E6756 Lab Assignment 3
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 1. Part 1 (40pts) Complete the utils/mtaupdates.py file.
# For complete credit, your code must include provisions to acquire all data
# from the MTA feed: tripUpdate, alert & vehicle messages (10 pts each). Also
# note that some tripIds appear in both the vehicle & tripUpdate message feeds,
# but they carry different information. The "trip_update" message feed
# typically carries general route information & the "vehicle" message update
# carries more 'current position' information. Your code MUST incorporate
# information from both feeds, where applicable (10 pts).
#

import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
import gtfs_realtime_pb2
import google.protobuf
import sys

import vehicle,alert,tripupdate

class mtaUpdates(object):

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')

    # Note that Feed_ID=1 applies to the 1,2,3,4,5,6 & Grand Central Shuttle
    MTA_FEED = 'http://datamine.mta.info/mta_esi.php?feed_id='

    # Initialize train ID
    TRAIN = "1"

    # Reading from the key file (you may need to change file path).
    with open('./key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()

    FEED_URL = MTA_FEED + TRAIN + '&key=' + APIKEY

    #VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}
    #tripUpdates = []
    #alerts = []

    #def __init__(self,apikey):
    #    self.FEED_URL = self.MTA_FEED + self.TRAIN + '&key=' + self.APIKEY

    # Method to get trip updates from mta real time feed
    def getTripUpdates(TRAIN, REQUEST):
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

        timestamp = feed.header.timestamp
        nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)

        update, vehicle, alert = "", "", ""
        u, v, a, = [], [], []
        vehicle_ctr, alert_ctr, trip_ctr=0,0,0

        for entity in feed.entity:
            # Trip update represents a change in timetable
            if entity.trip_update and entity.trip_update.trip.trip_id:
                update = entity
                #update = tripupdate.tripupdate()
                ##### INSERT TRIPUPDATE CODE HERE ####

            if entity.vehicle and entity.vehicle.trip.trip_id:
                v = entity
                #v = vehicle.vehicle()
                ##### INSERT VEHICLE CODE HERE #####

            if entity.alert:
                a = entity
                #a = alert.alert()
                #### INSERT ALERT CODE HERE #####

            if entity.HasField('trip_update'):
                #print entity
                trip_ctr=trip_ctr+1
            if entity.HasField('alert'):
                #print entity
                alert_ctr=alert_ctr+1
            if entity.HasField('vehicle'):
                #print entity
                vehicle_ctr=vehicle_ctr+1

        if REQUEST == 'alert':
            print a
            print "Alerts: ",    alert_ctr
        if REQUEST == 'vehicle':
            print v
            print "Vehicle Position Updates: ",vehicle_ctr
        if REQUEST == 'update':
            print update
            print "Trip Updates: ", trip_ctr
        else:
            print "Try Again"

        #return self.tripUpdates
        # END OF getTripUpdates method

print "Press Ctrl+C to escape..."
try:
    TRAIN=raw_input("What train are you taking? ")
    REQUEST=raw_input("update, vehicle, or alert? ")
    mtaUpdates().getTripUpdates(TRAIN,REQUEST)
except KeyboardInterrupt:
    exit
except:
    print "Error"
