#read the data from stream and post the predictedvalue to dynamodb

from __future__ import print_function
import boto3
import base64
import json

print('Loading function')

MODEL_ID = 'string'
COGNITO_ID = "EdisonApp"
def lambda_handler(event, context):
    kinesis = '{}'.format(event["Records"][0]["Data"]['dow (S)']+
    event["Records"][0]["Data"]['NinetySixArrive (S)']+
    event["Records"][0]["Data"]['routeId (S)'])
    client = getClient('machinelearning','us-east-1')
    r=predict(kinesis[7:-1],kinesis[:7],kinesis[-1],client)
    dynamodb = getResource('dynamodb', 'us-east-1')
    table = dynamodb.Table("mta2")
    table.update_item(
                        Key={
                            'NinetySixArrive':kinesis[7:-1]
                            },
                        UpdateExpression=
                            "set predictedValue=:a",
                            ExpressionAttributeValues={
                            ':a':str(r['Prediction']['predictedValue'])
                         })
         
    
def create_endpoint(client):
	try:
		response = client.create_realtime_endpoint(
			MLModelId=MODEL_ID
		)
		END_URL = response['RealtimeEndpointInfo']['EndpointUrl']
		return END_URL
	except KeyboardInterrupt:
		exit
		
def predict(num,mpm,dow,client):
	END_URL = create_endpoint(client)
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
	
def getCredentials():
	ACCOUNT_ID = '485969833300'
	IDENTITY_POOL_ID = 'us-east-1:b687bdd8-606d-464c-8e0c-eb42c6d79c1b'
	ROLE_ARN = 'arn:aws:iam::485969833300:role/Cognito_EdisonAppUnauth_Role'
	cognito = boto3.client('cognito-identity','us-east-1')
	cognito_id = cognito.get_id(AccountId=ACCOUNT_ID, IdentityPoolId=IDENTITY_POOL_ID)
	oidc = cognito.get_open_id_token(IdentityId=cognito_id['IdentityId'])
	sts = boto3.client('sts')
	assumedRoleObject = sts.assume_role_with_web_identity(RoleArn=ROLE_ARN,
	                     RoleSessionName=COGNITO_ID,
	                    WebIdentityToken=oidc['Token'])
	credentials = assumedRoleObject['Credentials']
	return credentials

def getClient(clientName,region):
	credentials = getCredentials()
	client = boto3.client(clientName,
			 region,
	        aws_access_key_id= credentials['AccessKeyId'],
	        aws_secret_access_key=credentials['SecretAccessKey'],
	        aws_session_token=credentials['SessionToken'])
	return client
	
def getResource(resourceName,region):
	credentials = getCredentials()
	resource = boto3.resource(resourceName,
			 region,
	        aws_access_key_id= credentials['AccessKeyId'],
	        aws_secret_access_key=credentials['SecretAccessKey'],
	        aws_session_token=credentials['SessionToken'])
	return resource
