#
# Populates out.csv with random values similar to temp values.
#
# print open('out.csv', 'rt').read()
#

import random
import time
import csv
import os.path

# create random number in temp range
def temp_rand():
    try:
        c = random.random()*50
        f = c * 9.0/5.0 + 32.0
        # ts = time.time()
        ts = time.strftime("%b %d %H:%M:%S")
        r = [ts, c, f]
        return r
    except KeyboardInterrupt:
        exit
    except:
        print "Random Gen Error"


print "Press Ctrl+C to escape..."
try:
    if os.path.exists('out.csv'):
        pass
    else:
        with open('out.csv','wb') as fout:
            writer = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(['timestamp','celsius','fahrenheit'])
    while True:
        with open('out.csv','a') as fout:
            writer = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
            # writer.writerow(['timestamp','celsius','fahrenheit'])
            table = temp_rand()
            writer.writerow(table)
            fout.close()
        time.sleep(1)
except KeyboardInterrupt:
        exit
except:
    print "Error in random.py"
