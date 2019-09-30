import json
import os
from hashlib import blake2s
import boto3
from aws_xray_sdk.core import xray_recorder

dynamodb = boto3.client('dynamodb')

@xray_recorder.capture("short_url")
def lambda_handler(event, context):
    if event["httpMethod"] == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : True,
                "Access-Control-Allow-Headers": "authorization, content-type"
            }
        }

    table_name = os.environ['TABLE_NAME']
    post_parameters = json.loads(event["body"])
    url_to_shorten = post_parameters['url']

    short_id = short_url(url_to_shorten)
    persist_mapping(short_id, table_name, url_to_shorten)

    return {
        "statusCode": 201,
        "body": json.dumps({
            "short_id": short_id
        }),
        "headers": {
            "Access-Control-Allow-Origin" : "*"
        }
    }

@xray_recorder.capture("persist_mapping")
def persist_mapping(short_id, table_name, url_to_shorten):
    dynamodb.put_item(
        TableName=table_name,
        Item={
            "short_id": {"S": short_id},
            "url": {"S": url_to_shorten},
        }
    )

@xray_recorder.capture("short_url")
def short_url(url_to_shorten):
    h = blake2s()
    h.update(bytes(url_to_shorten, 'utf-8'))
    short_id = "{:s}".format(h.hexdigest())
    return short_id
