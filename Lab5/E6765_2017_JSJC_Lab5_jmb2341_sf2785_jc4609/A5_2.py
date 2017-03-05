#
# 1. Based on the data collected in part 1, you may choose what input factors
# you think are critical to this choice of "switching" or not. For example,
# you may consider number of people at the station as a correlation metric for
# the performance of the trains. Perhaps, time of day may be a factor in
# evaluating whether waiting or switching is beneficial etc.
#
# 2. You need to create a AWS Machine Learning Model based on your choice of
# inputs and outputs. For example, you may choose Binary Classification as a
# mechanism to decide whether or not the local train reaches before the express
# trains. ('Yes' or 'No' binary). You may alternately choose the arrival time
# at 42nd street as the net result and derive the choice of train, based on
# this result. (Regression).
#
# 3. After creating your model, enable real-time predictions. To do this go to
# your learned ML model report page. Scroll to the bottom of the page and and
# click Create endpoint//. Note: this can only be done after creating your model.
#
# S3.S3('finalData.csv').uploadData()

from utils import S3

def uploadData():
	try:
		S3.S3('finalData.csv').uploadData()
		return True
	except KeyboardInterrupt:
		exit
	except:
		print "Data Upload Error"

# Factors that are important for deciding whether or not to switch at 96th:
# number of people at the station, time of day,

# AWS Machine Learning Model based on inputs and outputs
