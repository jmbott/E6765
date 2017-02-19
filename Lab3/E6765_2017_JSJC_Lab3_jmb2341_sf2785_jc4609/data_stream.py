#!/usr/bin/python
from protos import gtfs_realtime_pb2
import urllib,urllib2
import sys
import google.protobuf

TRAIN = str(1)

## Note that Feed_ID=1 applies to the 1,2,3,4,5,6 & Grand Central Shuttle
MTA_FEED = 'http://datamine.mta.info/mta_esi.php?feed_id='

## Reading from the key file (you may need to change file path).
with open('./utils/key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()

FEED_URL = MTA_FEED + TRAIN + '&key=' + APIKEY

## Using the gtfs_realtime_pb2 file created by the
## proto compiler, we view the feed using the method below.
feed = gtfs_realtime_pb2.FeedMessage()

try:
        response = urllib.urlopen(FEED_URL)
        d = feed.ParseFromString(response.read())
except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
        print "Error while connecting to mta server:\n " +str(e)

########################################################################
####### Run code above this point to validate your connection ##########
########################################################################

## As discussed, the MTA feed gives entities which give information regarding,
## vehicle status, trip_update information & alerts
## Walk through the code below for a quick introduction to the data feed.

vehicle_ctr, alert_ctr, trip_ctr=0,0,0

for entity in feed.entity:
        if entity.HasField('trip_update'):
                #print entity
                trip_ctr=trip_ctr+1
        if entity.HasField('alert'):
                #print entity
                alert_ctr=alert_ctr+1
        if entity.HasField('vehicle'):
                #print entity
                vehicle_ctr=vehicle_ctr+1

print "Trip Updates: ", trip_ctr
print "Alerts: ",    alert_ctr
print "Vehicle Position Updates: ",vehicle_ctr
