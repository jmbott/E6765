#
# IOT E6756 Lab Assignment 3
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# Part 2 (60pts)
# Using the code you developed in Part 1, complete the Lab3/dynamodata.py file.
#
# You are required to have 2 tasks running in parallel (20pts for
# multithreading + 30pts for the functionality):
# a. The first task, running every 30 sec, shall look at adding data to the
# "mtadata" DynamoDB table continuously.
# b. A second task, running every 60 sec, looks at cleaning out data from the
# table that is older than 2 minutes old.
#
# This should be implemented on the Intel Edison first. Since this should
# really be implemented on a cloud service, you must also port your code to a
# cloud service, using AWS EC2-based Virtual Machines. You must demonstrate
# functionality on both platforms for full credit.

import json, time, threading
from collections import OrderedDict
from threading import Thread

import boto3
from boto3.dynamodb.conditions import Key,Attr

from utils import tripupdate,vehicle,alert,aws

import A3_1

# *********************************************************************************************
# Program to update dynamodb with latest data from mta feed. It also cleans up stale entried from db
# Usage python A3_2.py
# *********************************************************************************************

client_dynamo = aws.getClient()

# Create DynamoDB item.
def create_item(name, item):
    # name must be string
    # item must be dict
    try:
        table = Table(name, connection=client_dynamo)
        table.put_item(data=item)
        return True
    except KeyboardInterrupt:
        exit

# Initialize begining times for threads
b1, b2 = 0, 0

def add():
    print threading.currentThread().getName(), 'Starting'
    time.sleep(2)
    print threading.currentThread().getName(), 'Exiting'

def clean():
    print threading.currentThread().getName(), 'Starting'
    time.sleep(3)
    print threading.currentThread().getName(), 'Exiting'

print "Press Ctrl+C to escape..."
try:
    while True:
        if b1 == 0:
            b1 = time.time()
            print b1
            t1= threading.Thread(name='add new data', target=add) # Define Threads
            t1.start() # Start thread t1
        if b2 == 0:
            b2 = time.time()
            print b2
            t2= threading.Thread(name='clean old data', target=clean) # Define Threads
            t2.start() # Start thread t2
        if time.time() - b1 > 30:
            b1 = 0
        if time.time() - b2 > 60:
            b2 = 0
except KeyboardInterrupt:
    exit
except:
    print "Error"
