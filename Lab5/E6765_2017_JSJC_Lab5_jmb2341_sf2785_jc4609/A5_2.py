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

from utils import S3

# upload data from csv in repo to S3
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
#
# Predict  ArriveTimesSquare based on categorical dow, catagorical route_id
# and NinetySixArrive time. Can estimate arrival at 96th based on
# train estimates from 116th
#
# AWS Machine Learning Model based on inputs and outputs

import time,sys,random
import boto3
from utils import aws
from datetime import datetime, date

TIMESTAMP  =  time.strftime('%Y-%m-%d-%H-%M-%S')
S3_BUCKET_NAME = "mtaedisondata2341"
S3_FILE_NAME = 'finalData.csv'
S3_URI = "s3://{0}/{1}".format(S3_BUCKET_NAME, S3_FILE_NAME)
DATA_SCHEMA = '{"version":"1.0","rowId":null,"rowWeight":null,"targetAttributeName":"TimesSquareArrive (S)","dataFormat":"CSV","dataFileContainsHeader":true,"attributes":[{"attributeName":"tripId (S)","attributeType":"NUMERIC"},{"attributeName":"NinetySixArrive (S)","attributeType":"NUMERIC"},{"attributeName":"TimesSquareArrive (S)","attributeType":"NUMERIC"},{"attributeName":"dow (S)","attributeType":"CATEGORICAL"},{"attributeName":"routeId (S)","attributeType":"CATEGORICAL"},{"attributeName":"ts (N)","attributeType":"NUMERIC"}],"excludedAttributeNames":[]}'
SOURCE_ID = 'ds_id347' #+ str(random.randint(0,1000))
MODEL_ID = 'ml_id347' #+ str(random.randint(0,1000))
EVAL_ID = 'ev_id'
EVAL_SCHEMA = '{"version":"1.0","rowId":null,"rowWeight":null,"targetAttributeName":"TimesSquareArrive (S)","dataFormat":"CSV","dataFileContainsHeader":true,"attributes":[{"attributeName":"tripId (S)","attributeType":"NUMERIC"},{"attributeName":"NinetySixArrive (S)","attributeType":"NUMERIC"},{"attributeName":"TimesSquareArrive (S)","attributeType":"NUMERIC"},{"attributeName":"dow (S)","attributeType":"CATEGORICAL"},{"attributeName":"routeId (S)","attributeType":"CATEGORICAL"},{"attributeName":"ts (N)","attributeType":"NUMERIC"}],"excludedAttributeNames":[]}'


client = aws.getClient('machinelearning','us-east-1')

def create_datasource():
	try:
		response = client.create_data_source_from_s3(
		    DataSourceId=SOURCE_ID,
		    DataSourceName='Final Data',
		    DataSpec={
		        'DataLocationS3': S3_URI,
		        #'DataRearrangement': 'string',
		        'DataSchema': DATA_SCHEMA,
		        #'DataSchemaLocationS3': 'string'
		    },
		    ComputeStatistics=True
		)
		return True
	except KeyboardInterrupt:
		exit


def create_ml():
	try:
		response1 = create_datasource()
		response2 = client.create_ml_model(
		    MLModelId=MODEL_ID,
		    MLModelName='Final Data',
		    MLModelType='REGRESSION',
		    #Parameters={
		    #    'string': 'string'
		    #},
		    TrainingDataSourceId=SOURCE_ID,
		    #Recipe='string',
		    #RecipeUri='string'
		)
		return True
	except KeyboardInterrupt:
		exit

def create_endpoint():
	try:
		response = client.create_realtime_endpoint(
			MLModelId=MODEL_ID
		)
		r = str(response)
		END_URL = r[214:270]
		return END_URL
	except KeyboardInterrupt:
		exit

def create_evaluation():
	response = client.create_evaluation(
	    EvaluationId=EVAL_ID,
	    EvaluationName='Final Data',
	    MLModelId=MODEL_ID,
	    EvaluationDataSourceId='string'
	)

def predict(num,mpm,dow):
	END_URL = create_endpoint()
	response = client.predict(
	    MLModelId=MODEL_ID,
	    Record={
	        'NinetySixArrive (S)': str(mpm),
			'dow (S)': str(dow),
			'routeId (S)': str(num)
	    },
	    PredictEndpoint=END_URL
	)
	return response

def switch():
	try:
		create_ml()
		ts = int(time.time()) - 18000
		hour = int(datetime.fromtimestamp(int(ts)).strftime('%H'))
		minute = int(datetime.fromtimestamp(int(ts)).strftime('%M'))
		# Timestamp in minutes past midnight
		mpm = hour*60 + minute
		today = date.fromtimestamp(ts)
		dow = date.weekday(today)
		if dow == 5 or dow == 6:
			dow = "weekend"
		else:
			dow = "weekday"
		r_1 = predict('1',mpm,dow)
		r_2 = predict('2',mpm,dow)
		r_3 = predict('3',mpm,dow)
		r_1 = str(r_1)
		r_2 = str(r_2)
		r_3 = str(r_3)
		a_1 = int(float(r_1[36:49]))
		a_2 = int(float(r_2[36:49]))
		a_3 = int(float(r_3[36:49]))
		if a_1 >= a_2 and a_1 >= a_3:
			o = a_1
			m = "Stay on local"
		elif a_2 >= a_3:
			o = a_3
			m = "Switch to express"
		else:
			o = a_2
			m = "Switch to express"
		out = o - mpm
		print "Estimated time in minutes from 96th to 42nd"
		print out
		print ""
		return m
	except KeyboardInterrupt:
	    exit

#print "Press Ctrl+C to escape..."
try:
	out = switch()
	print out
except KeyboardInterrupt:
    exit
except:
    print "Error"
