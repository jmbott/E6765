import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
from protos import gtfs_realtime_pb2
import google.protobuf
import sys
import time

#from utils import vehicle,alert,tripupdate

class mtaUpdates:

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')
    print "1"
    print TIMEZONE

    # Note that Feed_ID=1 applies to the 1,2,3,4,5,6 & Grand Central Shuttle
    MTA_FEED = 'http://datamine.mta.info/mta_esi.php?feed_id='

    print "2"
    print MTA_FEED

    # Reading from the key file (you may need to change file path).
    with open('./utils/key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()

    def __init__(self, FEED=1):
        self.FEED = str(FEED)
        self.FEED_URL = self.MTA_FEED + self.FEED + '&key=' + self.APIKEY
        self.d = OrderedDict()
        print "3"
        print self.FEED


    print "4"
    print self.FEED_URL

    #VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        ## Using the gtfs_realtime_pb2 file created by the
        ## proto compiler, we view the feed using the method below.
        feed = gtfs_realtime_pb2.FeedMessage()

        print "5"
        print feed
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

        print "6"
        print self.nytime

        try:
            for entity in feed.entity:

                # Initial Ordered Dict

                self.d['tripId'] = 'None'
                self.d['routeId'] = 'None'
                self.d['startDate'] = 'None'
                self.d['direction'] = 'None'
                self.d['currentStopId'] = 'None'
                self.d['currentStopStatus'] = 'None'
                self.d['vehicleTimeStamp'] = 'None'
                self.d['futureStopData'] = 'None'
                self.d['timestamp'] = str(time.time())

                # timeStamp: Feed timestamp [EDIT: This timestamp can be
                #  obtained from the mta feed's header message]
                self.d['timestamp'] = feed.header.timestamp

                if entity.HasField('trip_update'):

                    e = entity
                    # id = e.id

                    # tripId: The unique trip identifier
                    self.d['tripId'] = e.trip_update.trip.trip_id

                    # routeId: Train Route, eg, 1, 2, 3 etc. or "S" for the Grand
                    #  Shuttle Service between Times Square & Grand Central
                    self.d['routeId'] = e.trip_update.trip.route_id

                    # startDate: Journey Start Date
                    self.d['startDate'] = e.trip_update.trip.start_date

                    # direction: "N" or "S" depending on whether the journey is
                    #  uptown or downtown, respectively. (on the Grand Central
                    #  Shuttle, N: Times Square to Grand Central, S: reverse trip)
                    self.d['direction'] = e.trip_update.trip.trip_id[10:11]

                    # Message feed, regarding the message itself.
                    # futureStopData: Information from the trip_update message.
                    #  Should contain:
                    #  {<stop_id>: ["arrivaltime": <arrival_at_stop>, "departuretime": <departure_from_stop>]}
                    #  for eg.
                    #  {"247N": [{"arrivalTime":1454802090}, {"departureTime": 1454802090}], "246N": [{"arrivalTime": 1454802210}, {"departureTime": 1454802210}]}
                    self.d['futureStopData'] = str(e.trip_update.stop_time_update)

                if entity.HasField('vehicle'):

                    e = entity

                    # currentStopId: Applicable to vehicle messages, stop ID info.
                    self.d['currentStopId'] = e.vehicle.stop_id

                    # currentStopStatus:
                    #  {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"},
                    #  refer manual for more details.
                    self.d['currentStopStatus'] = e.vehicle.current_status # ?????

                    # vehicleTimeStamp: The time stamp obtained from the vehicle
                    self.d['vehicleTimeStamp'] = e.vehicle.timestamp
        except:
            print "Parsing Error"

        return self.d
        # END OF getTripUpdates method
