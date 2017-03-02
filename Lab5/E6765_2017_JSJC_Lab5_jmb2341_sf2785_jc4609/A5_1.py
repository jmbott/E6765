#
# Part 1: DATA ACQUISITION & CLEANING (10pts Data + 10pts Data cleaning):
#
# Generate data pts for atleast 3 days worth of data (you do NOT have to
# run it continuously, although that would give you a lot of data to work with.
# Just a few hours each day. The idea is to populate as much data as you can
# before you create your ML model.), preferably including a weekend. Keep
# appending this data to a .csv file. Clean the data to ensure you have updates
# for only those trains that are currently running. Further eliminate duplicate
# entries.
# Additionally, store this data to the S3 storage.
#

import datetime

# Unix time is # of seconds since January 1, 1970 00:00 UTC
hour = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%H'))
minute = int(datetime.datetime.fromtimestamp(int(ts)).strftime('%M'))
# Timestamp in minutes past midnight
m = hour*60 + minute


# tripId/train start time
# tripId: Constructed from the scheduled start time of the trip and a shape_id:
# <start time>_<shape_id>. The start time is represented as hundredths of
# minutes past midnight, six digits 0 padded. So, 6:45:30am would be
# 040550.
# 405.5/60 = 6 Remainder 0.7583
# 0.7583*60 = 45 Remainder 0.49
# minutes past midnight > parsed start time bit bit shifted into a float

# routeId, local or express train

# day of the week, weekday or Weekend

# Time at which it reaches express station (at 96th street)
# taken from the "vehicle message" of the MTA feed when possible
# alt from "arrival time" from the 'trip_update' message

# Time at which it reaches the destination (at 42nd Street)
# taken from the "vehicle message" of the MTA feed when possible
# alt from "arrival time" from the 'trip_update' message
