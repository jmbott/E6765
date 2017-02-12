#
# IOT E6756 Lab Assignment 1
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 1. (10pts) Demonstrate a working example of the Firebase interface,
# which involves you posting data to the Firebase.
# You should be able to work with the code provided.
#
# To read the database
# > python A2_JSJC_#1.py --read
#
# To post to the database
# > python A2_JSJC_#1.py --post <data string of dict>
# ex:
# > python A2_JSJC_#1.py --post '{"Edison":10}'
# > python A2_JSJC_#1.py --post '{"Edison":10, "Name":"anon", "UNI":"anon1234"}'
#

from firebase import firebase
import json
import argparse
import ast

# disable warnings from old python version
# REF: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
import requests.packages.urllib3 as urllib3
urllib3.disable_warnings()

# initialize database domain
domain = 'https://iot-e6765-jsjc.firebaseio.com/'

# Add domain for firebase database
firebase = firebase.FirebaseApplication(domain,None)

def read_data():
    try:
        result  = firebase.get('',None)
        return result
    except KeyboardInterrupt:
        exit

def post_data(path,data):
    try:
        post = firebase.post(path,data)
        return post
    except KeyboardInterrupt:
        exit

def delete_data(path,data):
    try:
        firebase.delete(path,data)
    except KeyboardInterrupt:
        exit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Posts or reads/retrieves data from Firebase')
    parser.add_argument('--read', action='store_true',
        help='Reads database and returns a JSON object')
    parser.add_argument('--post', metavar=('str(path)', 'str(dict(data))'),
        type=str, nargs=2, help='Posts data to firebase, must be strings')
    parser.add_argument('--delete', metavar=('str(path)', 'str(dict(data))'),
        type=str, nargs=2, help='Removes data from firebase, must be strings')
    args = parser.parse_args()

    if args.read:
        out = read_data()
    elif args.post:
        path = args.post[0]
        d = args.post[1]
        # print(d) # for debug
        data = ast.literal_eval(p)
        out = post_data(path,data)
    elif args.delete:
        path = args.delete[0]
        d = args.delete[1]
        # print(d) # for debug
        data = ast.literal_eval(p)
        out = delete_data(path,data)
    else:
        out = read_data()
    print(json.dumps(out))
