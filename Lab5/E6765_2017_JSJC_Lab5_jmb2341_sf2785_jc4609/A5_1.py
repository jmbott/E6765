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

from utils import mtaUpdates

mtaUpdates.mtaUpdates().getTripUpdates()
