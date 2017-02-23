import boto.sns
import logging
from utils import aws

# Get the service resource.
resource = aws.getResource('sns', 'us-east-1')

table = dynamodb.Table(name)
table.put_item(Item=item)


logging.basicConfig(filename="sns-publish.log", level=logging.DEBUG)

c = boto.sns.connect_to_region("us-east-1")

topicarn = "arn:aws:sns:us-east-1:811222862937:mtaSub"
message = "hello Mr"
message_subject = "trialBotoTRopic"

publication = c.publish(topicarn, message, subject=message_subject)

print publication
