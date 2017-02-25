#
# IOT E6756 Lab Assignment 4
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# Question 2 (80 pts)
# This week's exercise builds on what you have developed last week. Do run your
# solution to Assignment 3 to populate your table. Alternately, incorporate
# that code into your solution for this week. There are no points for either
# approach.
#
# Your source station is 116th Street, Columbia University (Station ID: 117S).
# Destination station is 42nd Street, Times Square (Station ID: 127S).
#
# You must create an interactive menu this week with 3 options.
# >> Plan trip: (Generate a notification on whether to "Switch" or "Stay" at
# the 96th Station)
# >> Subscribe to message feed: (Ask the user for his/her phone number & send
# a subscription message to the same)
# >> Exit (Exit and close program)


# 1. (10 pts) Get a list of local trains (ie, 1 trains) passing through the
# 96th station
# 2. (10 pts) Repeat the same for express trains (ie, 2 or 3 trains)
# 3. (10 pts) After you reach 96th from your source station find & display
# tripId of earliest local train reaching the 96th station.
# 4. (10 pts) Repeat 3. for express trains.
# 5. (10 pts) Print time taken to reach 42nd in each case. ("time" = time from
# source station to destination station)
# 6. (10 pts) Print whether user should "Switch to Express Train" or "Stay on
# in the Local Train", and send this to all your subscribers.
# 7. (10 pts) Error Handling
# 8. (10 pts)Generalize such that you could select any source station (on the
# local 1 train line) North of the 96th Street stop while heading downtown.
# Additionally, allow for a journey uptown from 42nd Street to any stop North
# of 96th Street. Essentially, you will choose whether or not to get on the
# express at 42nd Street. If you choose to get on the express, you will have
# to get off at 96th Street.
#


# Get a list of local or express trains passing through the 96th station
def list_trains(speed):
    try:

        return True
    except KeyboardInterrupt:
            exit
    except:
        print "Error listing trains"

# Find and display tripId of earliest train reaching the 96th station
def list_earliest(train_type):
    try:

        return True
    except KeyboardInterrupt:
            exit
    except:
        print "Error listing earliest train"

# Print time taken to reach 42nd on a local or express train
def time_to_times_square(train_type):
    try:

        return True
    except KeyboardInterrupt:
        exit
    except:
        print "Error getting time to"

# Flexible decision whether or not to switch at 96th st
def switch_decision(origin,destination):
    try:

        return True
    except KeyboardInterrupt:
        exit
    except:
        print "Error in switch decision"

def publish(subject,message):
    try:
        response = client.publish(
            TopicArn='arn:aws:sns:us-east-1:811222862937:mtaSub',
            #TargetArn='string',
            #PhoneNumber='string',
            Message=str(message),
            Subject=str(subject),
            #MessageStructure='string',
            #MessageAttributes={
                #'string': {
                    #'DataType': 'string',
                    #'StringValue': 'string',
                    #'BinaryValue': b'bytes'
                #}
            #}
        )
        return True
    except KeyboardInterrupt:
            exit
    except:
        print "Error Publishing"

menu = {}
menu['1']="List trains passing 96th going south from 116th"
menu['2']="List tripId of earliest train at 96th going south from 116th"
menu['3']="Time to reach 42nd going south from 116th"
menu['4']="Send trip decision to SNS subscribers from 116th to Times Square"
menu['5']="Flexible switch decision"
menu['6']="Exit"

print "Press Ctrl+C to escape..."
try:
    while True:
        options=menu.keys()
        options.sort()
        for entry in options:
            print entry, menu[entry]
        selection=raw_input("Please Select:")
        print ""
        # list trains passing 96th
        if selection =='1':
            speed=raw_input("List local or express trains?")
            print ""
            list_trains(speed)
            print ""
        # Find and display tripId of earliest train reaching the 96th station
        elif selection == '2':
            train_type=raw_input("On local, express, or overall train?")
            print ""
            list_earliest(train_type)
            print ""
        # Print time taken to reach 42nd for local or express train
        elif selection == '3':
            train_type=raw_input("On local or express train?")
            print ""
            time_to_times_square(train_type)
            print ""
        # "Switch to Express Train" or "Stay on in the Local Train"
        # Send to SNS subscribers
        elif selection == '4':
            time_local = list_earliest('local')
            time_express = list_earliest('express')
            print ""
            if train_local < time_express:
                print "Stay on in the Local Train"
                publish("Train Choice","Stay on in the Local Train")
            if train_local > time_express:
                print "Switch to Express Train"
                publish("Train Choice","Switch to Express Train")
            else:
                print "The elusive tie, stay on in the Local Train"
                publish("Train Choice","The elusive tie, stay on in the Local Train")
            print ""
        # Flexible decision whether or not to switch at 96th st
        elif selection == '5':
            origin = raw_input("From what station?")
            destination = raw_input("To what station?")
            switch_decision(origin,destination)
            print ""
        # exit
    elif selection == '6':
            break
        else:
            print "Unknown Option Selected!"
            print ""
except KeyboardInterrupt:
        exit
except:
    print "Error in Main Loop"


# Deal with it if there is nothing in the database
# Deal with it if there is not a database
