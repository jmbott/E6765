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

# You are required to do the following tasks for full credit:
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
