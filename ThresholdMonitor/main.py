import json
import boto3
import datetime
from boto3.dynamodb.conditions import Key
import time
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tweets')
sqs = boto3.client('sqs')
queue_url = 'SLACK'

KEYWORDS=  [' bubble closed', 'screw', 'closed']

def get_date_code():
    now = datetime.now()
    date_code = now.strftime("%Y%m%d") 
    return date_code

def get_time_window(minutes):
    window_end = time.time_ns()
    window_start = window_end - (60000000000 * minutes)
    return window_start, window_end

def query_dynamo():
    while True:
        if not table.global_secondary_indexes or table.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
            print('Waiting for index to backfill...')
            time.sleep(5)
            table.reload()
        else:
            break

    window_start, window_end = get_time_window(5)
    date_code = get_date_code()
    response = table.query(
        IndexName='tweet_datecode-tweet_time-index',
        KeyConditionExpression=Key('tweet_datecode').eq(date_code) & Key('tweet_time').between(window_start, window_end),
        ScanIndexForward=False
    )

    return response

def publish_alert_sqs(alert_threshold, alert_tweets):
    print(f'REPORT : {alert_threshold} tweets alerting in period')
    print(alert_tweets)
    response = sqs.send_message(
    QueueUrl=queue_url,
    MessageAttributes={
        'alert_threshold': {
            'DataType': 'String',
            'StringValue': str(alert_threshold)
        }
    },
    MessageBody=(str(alert_tweets))
    )

    print(response['MessageId'])

def analyse_records():
    alert_threshold = 0
    alert_tweets = []
    tweets = query_dynamo()
    for tweet in tweets['Items']:
        tweet_body = tweet['tweet_body']
        for keyword in KEYWORDS:
            if keyword in tweet_body:
                print(f'MATCH : found {keyword} in {tweet_body}')
                alert_threshold += 1
                alert_tweets.append({"tweet" : tweet_body, "tweeter" : '@Bloggs'})
    
    if alert_threshold > 0:
        publish_alert_sqs(alert_threshold, alert_tweets)


def lambda_handler(event, context):
    analyse_records()