#
# IOT E6756 Lab Assignment 1
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 1. (10pts) Demonstrate a working example of the Firebase interface,
# which involves you posting data to the Firebase.
# You should be able to work with the code provided.
#

from firebase import firebase
import json as simplejson

# Add domain for firebase database
firebase = firebase.FirebaseApplication('https://iot-e6765-jsjc.firebaseio.com/',None)

def read_data():
    try:
        result  = firebase.get('',None)
        print result
    except KeyboardInterrupt:
        exit

def post_data(data):
    try:
        # d = simplejson.dumps(data)
        # print d
        post = firebase.post('',data)
        print post
    except KeyboardInterrupt:
        exit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Posts or reads/retrieves data from Firebase')
    parser.add_argument('--read', action='store_true',
        help='Reads database and returns a JSON object')
    parser.add_argument('--post', metavar='data',
        type=str, nargs=1, help='Posts data to firebase')
    args = parser.parse_args()

    if args.read:
        out = read_data()
    elif args.post:
        data = args.post[0]
        out = post_data(data)
    else:
        out = read_data()
    print(json.dumps(out))
