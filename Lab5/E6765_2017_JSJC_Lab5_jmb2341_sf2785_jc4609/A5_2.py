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
from datetime import datetime

TIMESTAMP  =  time.strftime('%Y-%m-%d-%H-%M-%S')
S3_BUCKET_NAME = "mtaedisondata2341"
S3_FILE_NAME = 'finalData.csv'
S3_URI = "s3://{0}/{1}".format(S3_BUCKET_NAME, S3_FILE_NAME)
DATA_SCHEMA = '{"version":"1.0","rowId":null,"rowWeight":null,"targetAttributeName":"TimesSquareArrive (S)","dataFormat":"CSV","dataFileContainsHeader":true,"attributes":[{"attributeName":"tripId (S)","attributeType":"NUMERIC"},{"attributeName":"NinetySixArrive (S)","attributeType":"NUMERIC"},{"attributeName":"TimesSquareArrive (S)","attributeType":"NUMERIC"},{"attributeName":"dow (S)","attributeType":"CATEGORICAL"},{"attributeName":"routeId (S)","attributeType":"CATEGORICAL"},{"attributeName":"ts (N)","attributeType":"NUMERIC"}],"excludedAttributeNames":[]}'
SOURCE_ID = 'ds_id'
MODEL_ID = 'ml_id'
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
		END_URL = r[211:267]
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

print "Press Ctrl+C to escape..."
try:
	create_ml()
	num=raw_input("1, 2 or 3 train? ")
	dow=raw_input("Is it the weekend or a weekday? ")
	ts = int(time.time()) - 18000
	hour = int(datetime.fromtimestamp(int(ts)).strftime('%H'))
	minute = int(datetime.fromtimestamp(int(ts)).strftime('%M'))
	# Timestamp in minutes past midnight
	mpm = hour*60 + minute
	response = predict(num,mpm,dow)
	r = str(response)
	a = int(float(r[36:53]))
	out = a - mpm
	print "estimated time in minutes from 96th to 42nd"
	print out
except KeyboardInterrupt:
    exit
except:
    print "Error"
