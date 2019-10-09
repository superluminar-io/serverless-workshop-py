import os
import boto3
from aws_xray_sdk.core import xray_recorder

dynamodb = boto3.client('dynamodb')


@xray_recorder.capture("lambda_handler")
def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    short_id = event["pathParameters"]["short_id"]
    result = fetch_url(short_id, table_name)

    if not "Item" in result:
        return {"statusCode": 404}

    long_url = result["Item"]["url"]["S"]

    return {
        "statusCode": 301,
        "headers": {
            "location": long_url
        }
    }


@xray_recorder.capture("fetch_url")
def fetch_url(short_id, table_name):
    result = dynamodb.get_item(
        TableName=table_name,
        Key={
            "short_id": {"S": short_id}
        }
    )
    return result
