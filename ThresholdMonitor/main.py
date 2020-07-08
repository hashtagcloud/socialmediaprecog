import json
import boto3
from boto3.dynamodb.conditions import Key
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('demo-table')

def get_date_code():
    now = datetime.now()
    date_code = now.strftime("%Y%m%d") 
    return date_code


while True:
    if not table.global_secondary_indexes or table.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
        print('Waiting for index to backfill...')
        time.sleep(5)
        table.reload()
    else:
        break

resp = table.query(
    IndexName="year-time-index",
    KeyConditionExpression=Key('year').eq('2019') & Key('time').between(1593445000, 1593445222),
    ScanIndexForward=False
)

print("The query returned the following items:")
for item in resp['Items']:
    print(item)

def lambda_handler(event, context):
    pass