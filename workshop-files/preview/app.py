import os
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']

    for r in event["Records"]:
        url = r["dynamodb"]["NewImage"]["url"]["S"]
        dynamodb.put_item(
            TableName=table_name,
            Item={
                "url": {"S": url},
            }
        )

    return "ok"
