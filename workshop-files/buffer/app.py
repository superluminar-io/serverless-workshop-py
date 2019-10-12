import boto3
import json
import os

client = boto3.client('sqs')

def lambda_handler(event, context):
    queue_url = os.environ['QUEUE_URL']

    client.send_message(
        QueueUrl=queue_url,
        MessageBody="some data from the request",
    )
    return {
        "statusCode": 200,
        "body":  "ok",
    }
