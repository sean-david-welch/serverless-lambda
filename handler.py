import os
import json
import psycopg2

from dotenv import load_dotenv
from typing import Any, Dict
from queries import fetch_products

load_dotenv()

connection_params = {
    "host": os.environ["PGHOST"],
    "dbname": os.environ["PGDATABASE"],
    "user": os.environ["PGUSER"],
    "password": os.environ["PGPASSWORD"],
    "port": os.environ["PGPORT"],
}


def read_products(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    cursor = None
    connection = None

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        result = fetch_products(cursor)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Query executed", "data": result, "input": event}
            ),
        }

    except Exception as error:
        context.serverless_sdk.capture_exception(error)
        return {"statusCode": 500, "body": json.dumps({"message": str(error)})}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
