import os
import boto3
from link_preview import link_preview

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    for r in event["Records"]:
        url = r["dynamodb"]["NewImage"]["url"]["S"]
        dict_elem = link_preview.generate_dict(url)
        title = dict_elem['title']
        description = dict_elem['description']
        image = dict_elem['image']

        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                "url": {"S": url},
                "title": {"S": title},
                "description": {"S": description},
                "image": {"S": image},
            }
        )
    return "ok"
