import json
import boto3
import slack
import os

SLACK_TOKEN = os.environ.get('SLACK_TOKEN','')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL','')

def build_message_block(comment):
    message = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": comment
                    }
                    },
            ]
    return message

def post_to_slack(*args):
    build_message_block(comment)
    client = slack.WebClient(token=SLACK_TOKEN)
    post_message = build_message_block(url, comment)
    response = client.chat_postMessage(channel=SLACK_CHANNEL, blocks=post_message)

def lambda_handler(event, context):
    pass