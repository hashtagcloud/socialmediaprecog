import json
import boto3
from datetime import datetime


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('table')

def get_date_code():
    now = datetime.now()
    date_code = now.strftime("%Y%m%d") 
    return date_code

def write_to_dynamo(*args):
    table.put_item(
        Item={
                'id': arg[0],
                'tweet_body': arg[1],
                'tweet_time': arg[2],
                'tweet_datecode': arg[3]
            }
        )

def lambda_handler(event, context):
    for record in event['Records']:
        tweet_body = record['body']
        tweet_time = int(record['messageAttributes']['tweet_time']['stringValue'])
        tweet_id = record['messageAttributes']['id']['stringValue']
        tweet_datecode = get_date_code()
        write_to_dynamo(tweet_id, tweet_body, tweet_time, tweet_datecode)