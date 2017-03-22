#
# Populates database with values from python-weather-api
#
# Must be placed in ~/Lab6 (our django instance)
#

import pywapi
import time
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Lab6.settings'
import django
django.setup()

from a2.models import C, F
from django.utils import timezone

# read temp from location in weather api
def temp(station_id):
    try:
        r = str(pywapi.get_weather_from_noaa(str(station_id)))
        x = r.find('temp_c')
        y = r.find('temp_f')
        if x != -1:
            c = r[x+10:x+14]
        if y != -1:
            f = r[y+10:y+14]
        else:
            return False
        # ts = time.time()
        ts = time.strftime("%b %d %H:%M:%S")
        t = {'ts':ts,'C':c,'F':f}
        return t
    except KeyboardInterrupt:
        exit
    except:
        print("Random Gen Error")

def post(temp, city_id):
    try:
        c = C(temp_c=int(float(temp['C'][:-1])), city=city_id, pub_date=timezone.now())
        c.save()
        f = F(temp_f=int(float(temp['F'][:-1])), city=city_id, pub_date=timezone.now())
        f.save()
    except KeyboardInterrupt:
        exit
    except:
        print("Post Error")


print("Press Ctrl+C to escape...")
try:
#    if os.path.exists('out.csv'):
#        pass
#    else:
#        with open('out.csv','wb') as fout:
#            writer = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
#            writer.writerow(['timestamp','celsius','fahrenheit'])
    while True:
        # get temps
        ny_temp = temp('KNYC')
        no_temp = temp('KNBG')
        bs_temp = temp('KEKS')
        sf_temp = temp('KSFO')
        # post to database
        post(ny_temp, 1);
        post(no_temp, 2);
        post(bs_temp, 3);
        post(sf_temp, 4);
        time.sleep(30)
except KeyboardInterrupt:
        exit
except:
    print("Error in random.py")
