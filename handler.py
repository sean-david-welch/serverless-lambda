import os
import json
import psycopg2

from dotenv import load_dotenv
from typing import Any, Dict
from queries import fetch_products

load_dotenv()


def hello(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
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

        result = fetch_products(cursor)

        body = {"message": "Query executed", "data": result, "input": event}
        status_code = 200

    except Exception as error:
        body = {"message": str(error)}
        status_code = 500
        context.serverless_skd.capture_exception(error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    response = {"statusCode": status_code, "body": json.dumps(body)}
    return response
