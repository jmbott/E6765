#
# Gets and posts data from the Google Maps API
#

import googlemaps
from datetime import datetime

# setup
gmaps = googlemaps.Client(key='AIzaSyCbMoxSzeGC4-hsFAclI6bgEKzfpnEuatA')


geocode_result_sf = gmaps.geocode('San Francisco, CA')
geocode_result_ny = gmaps.geocode('New York, NY')
geocode_result_bs = gmaps.geocode('Big Sky, MO')
geocode_result_no = gmaps.geocode('New Orleans, LA')


source = 'Big Sky, MO'
destination = 'San Francisco, CA'
# Request directions via car
now = datetime.now()
directions_result = gmaps.directions(source,
                                     destination,
                                     mode="driving",
                                     departure_time=now)
