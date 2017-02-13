#
# IOT E6756 Lab Assignment 2
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# 2. (30pts) Design a simple program, using DynamoDB, that creates a table,
# allows the user to interactively add, delete or view all items in a DynamoDB
# table. The fields of entries could be "name", "CUID". Additionally, add a
# simple search feature that allows you to search through the table, by name
# or CUID (one or the other).
#

import boto
import boto.dynamodb2
import json
import argparse
import ast
import time
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey

# AWS Account Information
ACCOUNT_ID = '811222862937'
IDENTITY_POOL_ID = 'us-east-1:366af791-82c4-490a-8b3e-157a7b007ba2'
ROLE_ARN = 'arn:aws:iam::811222862937:role/Cognito_edisonDemoKinesisUnauth_Role'

# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])

# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

# Prepare DynamoDB client
client_dynamo = boto.dynamodb2.connect_to_region(
    'us-east-1',
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)

# Create the DynamoDB table.
def create_table(name,hashkey,rangekey):
    try:
        table = Table.create(name, schema=[HashKey(hashkey),RangeKey(rangekey)], connection=client_dynamo)
        print 'writing...'
        time.sleep(12)
        return True
    except KeyboardInterrupt:
        exit

# Creates table with name and uni schema
def name_uni_table():
    try:
        create_table('AssignmentTwo','name','CUID')
        return True
    except KeyboardInterrupt:
        exit

# Delete a DynamoDB table.
def delete_table(name):
    # input must be string
    try:
        table = Table(name, connection=client_dynamo)
        table.delete()
        return
    except KeyboardInterrupt:
        exit

# Count items in table.
def count_table(name):
    # input must be string, 6 hours delayed
    try:
        table = Table(name, connection=client_dynamo)
        count = table.count()
        return count
    except KeyboardInterrupt:
        exit

# Create DynamoDB item.
def create_item(name, item):
    # name must be string
    # item must be dict
    try:
        table = Table(name, connection=client_dynamo)
        table.put_item(data=item)
        return True
    except KeyboardInterrupt:
        exit

# Delete DynamoDB item for A2
def name_uni_delete_item(tbl, name, uni):
    # name must be string
    # item must be dict
    try:
        table = Table(tbl, connection=client_dynamo)
        table.delete_item(name=name, CUID=uni)
        return True
    except KeyboardInterrupt:
        exit

# Add prescribed name and UNI
def name_uni_item(name,CUID):
    try:
        # inputs must be strings
        create_item('AssignmentTwo',{'name':name, 'CUID':CUID})
        return True
    except KeyboardInterrupt:
        exit

# Describe table
def desc_table(name):
    # inputs must be strings
    try:
        table = Table(name, connection=client_dynamo)
        out = table.describe()
        print json.dumps(out, indent=4, sort_keys=True)
        return out
    except KeyboardInterrupt:
        exit

# View all entries in A2 table
def name_uni_list():
    try:
        table = Table('AssignmentTwo', connection=client_dynamo)
        result = table.scan()
        for n in result:
            print '{0:1} : {1:1}'.format(n['name'], n['CUID'])
        return
    except KeyboardInterrupt:
        exit

# Search by CUID in A2 table
def search_CUID(uni):
    # inputs must be strings
    try:
        table = Table('AssignmentTwo', connection=client_dynamo)
        result = table.scan(CUID__eq=uni)
        for n in result:
            print n['name']
        return
    except KeyboardInterrupt:
        exit

# Search by name in A2 table
def search_name(name):
    # inputs must be strings
    try:
        table = Table('AssignmentTwo', connection=client_dynamo)
        result = table.query_2(name__eq=name)
        for n in result:
            print n['CUID']
        return
    except KeyboardInterrupt:
        exit


# # Update an item (in progress)
# def update_table(name, item):
#     # input must be string
#     try:
#         table = Table(name)
#         item
#     except KeyboardInterrupt:
#         exit

 ################
"""

def read_data():
    try:
        result  = firebase.get('',None)
        return result
    except KeyboardInterrupt:
        exit

def post_data(path,data):
    try:
        post = firebase.post(path,data)
        return post
    except KeyboardInterrupt:
        exit

def delete_data(path):
    try:
        firebase.delete(path, None)
        return True
    except KeyboardInterrupt:
        exit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='posts or reads/retrieves data from Firebase')
    parser.add_argument('--read', action='store_true',
        help='reads database and returns a JSON object')
    parser.add_argument('--post', metavar=('str(path)', 'str(dict(data))'),
        type=str, nargs=2, help='posts data to Firebase, must be strings')
    parser.add_argument('--delete', metavar=('str(path)'),
        type=str, nargs=1, help='removes data from Firebase, must be string')
    args = parser.parse_args()

    if args.read:
        out = read_data()
    elif args.post:
        path = args.post[0]
        d = args.post[1]
        # print(d) # for debug
        data = ast.literal_eval(d)
        out = post_data(path,data)
    elif args.delete:
        path = args.delete[0]
        out = delete_data(path)
    else:
        out = read_data()
    print(json.dumps(out))
"""
