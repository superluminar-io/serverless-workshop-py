def lambda_handler(event, context):
    name = event["pathParameters"]["name"]

    return {
        "statusCode": 200,
        "body":  "hello {}".format(name)
    }
