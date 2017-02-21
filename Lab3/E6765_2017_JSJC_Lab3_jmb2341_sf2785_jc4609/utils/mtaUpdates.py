import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
from protos import gtfs_realtime_pb2
import google.protobuf
import sys

from utils import vehicle,alert,tripupdate

class mtaUpdates:

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')

    # Note that Feed_ID=1 applies to the 1,2,3,4,5,6 & Grand Central Shuttle
    MTA_FEED = 'http://datamine.mta.info/mta_esi.php?feed_id='

    # Reading from the key file (you may need to change file path).
    with open('./utils/key.txt', 'rb') as keyfile:
        APIKEY = keyfile.read().rstrip('\n')
        keyfile.close()

    def __init__(self, FEED=1):
        self.FEED = str(FEED)
        self.FEED_URL = self.MTA_FEED + self.FEED + '&key=' + self.APIKEY
        #self.update = tripupdate
        #self.vehicle = vehicle
        #self.alert = alert

    #VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self, REQUEST):
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
        # nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)

        self.vehicle_ctr, self.alert_ctr, self.trip_ctr = 0,0,0

        for entity in feed.entity:
            # Trip update represents a change in timetable

            if entity.HasField('trip_update'):
                print entity.trip_update.trip.trip_id
                print entity.trip_update.trip.route_id
                    self.updates.append(entity)

            if entity.HasField('vehicle'):
                # self.vehicle_ctr = self.vehicle_ctr + 1
                self.vehicle.append(entity)

            if entity.HasField('alert'):
                print entity.id
                print entity.alert.trip.trip_id
                print entity.alert.trip.route_id
                print entity.alert.translation.text
                self.alerts.append(entity)


            for entity in feed.entity:
                # Initial Ordered Dict
                d = OrderedDict()
                d['tripId'] = ''
                d['routeId'] = ''
                d['startDate'] = ''
                d['direction'] = ''
                d['currentStopId'] = ''
                d['currentStopStatus'] = ''
                d['vehicleTimeStamp'] = ''
                d['futureStopData'] = ''
                d['timestamp'] = ''
                # timeStamp: Feed timestamp [EDIT: This timestamp can be
                #  obtained from the mta feed's header message]
                ts = feed.header.timestamp
                if entity.HasField('trip_update'):
                    e = entity
                    id = e.id
                    # tripId: The unique trip identifier
                    d['tripId'] = e.trip_update.trip.trip_id
                    # routeId: Train Route, eg, 1, 2, 3 etc. or "S" for the Grand
                    #  Shuttle Service between Times Square & Grand Central
                    d['routeId'] = e.trip_update.trip.route_id
                    # startDate: Journey Start Date
                    d['startDate'] = e.trip_update.trip.start_date
                    # direction: "N" or "S" depending on whether the journey is
                    #  uptown or downtown, respectively. (on the Grand Central
                    #  Shuttle, N: Times Square to Grand Central, S: reverse trip)
                    d['direction'] = e.trip_update.trip.trip_id[10:11]
                    # Message feed, regarding the message itself.
                    # futureStopData: Information from the trip_update message.
                    #  Should contain:
                    #  {<stop_id>: ["arrivaltime": <arrival_at_stop>, "departuretime": <departure_from_stop>]}
                    #  for eg.
                    #  {"247N": [{"arrivalTime":1454802090}, {"departureTime": 1454802090}], "246N": [{"arrivalTime": 1454802210}, {"departureTime": 1454802210}]}
                    d['futureStopData'] = str(e.trip_update.stop_time_update)

                if entity.HasField('vehicle'):
                    e = entity
                    # currentStopId: Applicable to vehicle messages, stop ID info.
                    d['currentStopId'] = e.vehicle.stop_id
                    # currentStopStatus:
                    #  {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"},
                    #  refer manual for more details.
                    d['currentStopStatus'] = e.vehicle.current_status # ?????
                    # vehicleTimeStamp: The time stamp obtained from the vehicle
                    d['vehicleTimeStamp'] = e.vehicle.timestamp



                d = OrderedDict()
                d['a'] = 'A'
                d['b'] = 'B'
                d['c'] = 'C'
                d['d'] = 'D'
                d['e'] = 'E'

            #f = str(e.trip_update.stop_time_update)
            #f[93:97] # or f[44:48] for departure

        try:
            if REQUEST == 'u':
                return self.updates
                # print "Trip Updates: ", self.trip_ctr
            if REQUEST == 'v':
                return self.vehicle
                # print "Vehicle Position Updates: ", self.vehicle_ctr
            if REQUEST == 'a':
                return self.alerts
                # print "Alerts: ", self.alert_ctr
        except:
            print "Request Error"

        # END OF getTripUpdates method
