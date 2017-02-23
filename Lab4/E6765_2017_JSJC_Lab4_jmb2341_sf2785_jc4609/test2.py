import boto3
import logging
from utils import aws

# Setup Logging
#logging.basicConfig(filename="sns-publish.log", level=logging.DEBUG)

#client = boto3.client('sns', 'us-east-1')

# Get the service resource.
client = aws.getClient('sns', 'us-east-1')

response = client.publish(
    TopicArn='arn:aws:sns:us-east-1:811222862937:mtaSub',
    #TargetArn='string',
    #PhoneNumber='string',
    Message='test2',
    Subject='test2',
    #MessageStructure='string',
    #MessageAttributes={
        #'string': {
            #'DataType': 'string',
            #'StringValue': 'string'#,
            #'BinaryValue': b'bytes'
        #}
    #}
)
