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
# To combine csv outputs from dynamodb you must strip the headers from subsiquent
# files and print them to a final location
# $ sed 1d "mtadata5 (1).csv" > file2noheader.csv
# $ sed 1d "mtadata5 (2).csv" > file3noheader.csv
# $ sed 1d "mtadata5 (3).csv" > file4noheader.csv
# $ cat mtadata5.csv file2noheader.csv file3noheader.csv file4noheader.csv file5noheader.csv > finalData.csv
#

from utils import mtaUpdates
import time
import sys

update = []

while True:

    f = open("A5_1.out", 'w')
    update.append(mtaUpdates.mtaUpdates().getTripUpdates())
    print >> f, update
    f.close()
    time.sleep(60)
