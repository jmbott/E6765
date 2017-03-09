# This program sends the data to kinesis. You do not need to modify this code except the Kinesis stream name.
# Usage python pushToKinesis.py <file name>
# a lambda function will be triggered as a result, that will send it to AWS ML for classification
# Usage python pushToKinesis.py <csv file name with extension>

import sys,csv,json

import boto3

sys.path.append('../utils')
from utils import aws


KINESIS_STREAM_NAME = 'mtastream'
kinesis = aws.getClient('kinesis','us-east-1')

def main(fileName):

    # connect to kinesis
    data = [] # list of dictionaries will be sent to kinesis
    with open(fileName,'rb') as f:
    	dataReader = csv.DictReader(f)
        for row in dataReader:
            kinesis.put_record(StreamName=KINESIS_STREAM_NAME, Data=json.dumps(row), PartitionKey='0')
            break
        f.close()




if __name__ == "__main__":
    
    try:
        fileName = "finalData-slim.csv"
        main(fileName)
        Iterator = kinesis.get_shard_iterator(
                    StreamName='mtastream',
                    ShardId='shardId-000000000000',
                    ShardIteratorType='TRIM_HORIZON'
                    )
        response = kinesis.get_records(
                      ShardIterator=Iterator['ShardIterator'],
                      Limit=2
                      )
        print response
    except Exception as e:
        raise e
