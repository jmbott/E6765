#
# Populates database with values from python-weather-api
#

import pywapi
import time

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

        time.sleep(30)
except KeyboardInterrupt:
        exit
except:
    print("Error in random.py")
