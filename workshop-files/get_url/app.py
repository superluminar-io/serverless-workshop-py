import os

import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    short_id = event["pathParameters"]["short_id"]
    result = dynamodb.get_item(
        TableName=table_name,
        Key={
            "short_id": {"S": short_id}
        }
    )

    if not "Item" in result:
        return {"statusCode": 404}

    long_url = result["Item"]["url"]["S"]

    return {
        "statusCode": 301,
        "headers": {
            "location": long_url
        }
    }
