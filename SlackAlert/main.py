import json
import boto3
import slack
import os

#SLACK_TOKEN = os.environ.get('SLACK_TOKEN','')
#SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL','')

SLACK_TOKEN = ''
SLACK_CHANNEL = 'customertweets'

def build_message_block(*args):
    message = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'Tweet threshold met, found {args[0]} tweets <br> {args[1]}'
                    }
                    },
            ]
    return message

def post_to_slack(*args):
    client = slack.WebClient(token=SLACK_TOKEN)
    post_message = build_message_block(args[0], args[1])
    response = client.chat_postMessage(channel=SLACK_CHANNEL, blocks=post_message)

def lambda_handler(event, context):
    for record in event['Records']:
        tweet_body = record['body']
        threshold = record['messageAttributes']['alert_threshold']['stringValue']
        post_to_slack(threshold, tweet_body)