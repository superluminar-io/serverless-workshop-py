import os
import boto3
from webpreview import web_preview

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']

    for r in event["Records"]:
        url = r["dynamodb"]["NewImage"]["url"]["S"]
        title, description, image = web_preview(url)
        dynamodb.put_item(
            TableName=table_name,
            Item={
                "url": {"S": url},
                "title": {"S": title},
                "description": {"S": description},
                "image": {"S": image},
            }
        )

    return "ok"
