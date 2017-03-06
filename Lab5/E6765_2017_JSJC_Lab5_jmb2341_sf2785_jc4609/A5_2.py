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

# Predict  ArriveTimesSquare based on categorical dow, catagorical route_id
# and ArriveNinetySix time

# AWS Machine Learning Model based on inputs and outputs

import time,sys,random
import boto3
from utils import aws

TIMESTAMP  =  time.strftime('%Y-%m-%d-%H-%M-%S')
S3_BUCKET_NAME = "mtaedisondata2341"
S3_FILE_NAME = 'finalData.csv'
S3_URI = "s3://{0}/{1}".format(S3_BUCKET_NAME, S3_FILE_NAME)
DATA_SCHEMA = '{"version":"1.0","rowId":null,"rowWeight":null,"targetAttributeName":"TimesSquareArrive (S)","dataFormat":"CSV","dataFileContainsHeader":true,"attributes":[{"attributeName":"tripId (S)","attributeType":"NUMERIC"},{"attributeName":"NinetySixArrive (S)","attributeType":"NUMERIC"},{"attributeName":"TimesSquareArrive (S)","attributeType":"NUMERIC"},{"attributeName":"dow (S)","attributeType":"CATEGORICAL"},{"attributeName":"routeId (S)","attributeType":"CATEGORICAL"},{"attributeName":"ts (N)","attributeType":"NUMERIC"}],"excludedAttributeNames":[]}'
SOURCE_ID = 'ds_id'

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
		return response
	except KeyboardInterrupt:
		exit


def create_ml():
	try:
		source_id = create_datasource()
		response = client.create_ml_model(
		    MLModelId='ml_id',
		    MLModelName='Final Data',
		    MLModelType='REGRESSION',
		    #Parameters={
		    #    'string': 'string'
		    #},
		    TrainingDataSourceId=SOURCE_ID,
		    #Recipe='string',
		    #RecipeUri='string'
		)
	except KeyboardInterrupt:
		exit
