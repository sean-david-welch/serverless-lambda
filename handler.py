import os
import json
import boto3
import pyodbc


def hello(event, context):
    body = {"message": "Hi there, this is a test lambda function", "input": event}

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
