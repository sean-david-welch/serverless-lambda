import os
import json
import boto3
import psycopg2
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv()


def hello(event, context):
    cursor = None
    connection = None

    try:
        connection = psycopg2.connect(
            host=os.environ["PGHOST"],
            dbname=os.environ["PGDATABASE"],
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"],
            port=os.environ["PGPORT"],
        )

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "Product"')
        result = cursor.fetchall()

        body = {"message": "Query executed", "data": result, "input": event}
        status_code = 200

    except Exception as error:
        body = {"message": str(error)}
        status_code = 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    response = {"statusCode": status_code, "body": json.dumps(body)}
    return response
