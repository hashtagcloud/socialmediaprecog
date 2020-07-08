import json
import boto3
import random
import time
import uuid

sqs = boto3.client('sqs')
queue_url = 'TWEETS'

random_words = ["fan","uncertainty","chain","precedent","hook","inflation","machinery",
"training","lend","reform","fence","wrist","dump","sign","bubble",
"closed","warn","cabin","measure","screw"]

def random_phase_generator():
    def random_word():
        return random.choice(random_words)
    random_phrase = f'{random_word()} {random_word()} {random_word()}'
    return random_phrase

def post_to_sqs(message):
    response = sqs.send_message(
    QueueUrl=queue_url,
    MessageAttributes={
        'Test': {
            'DataType': 'String',
            'StringValue': message
        },
        'Time': {
            'DataType': 'String',
            'StringValue': str(time.time_ns())
        },
        'id': {
            'DataType': 'String',
            'StringValue': str(uuid.uuid1())
        }
    },
    MessageBody=(message)
    )

    print(response['MessageId'])


def lambda_handler(event, context):
    for i in range(3):
        message = random_phase_generator()
        post_to_sqs(message)
