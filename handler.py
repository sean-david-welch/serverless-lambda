import os
import json
import psycopg2

from dotenv import load_dotenv
from typing import Any, Dict
from queries import fetch_products, create_product

load_dotenv()

connection_params = {
    "host": os.environ["PGHOST"],
    "dbname": os.environ["PGDATABASE"],
    "user": os.environ["PGUSER"],
    "password": os.environ["PGPASSWORD"],
    "port": os.environ["PGPORT"],
}


def get_products(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
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


def post_product(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    cursor = None
    connection = None

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        body = json.loads(event.get("body", "{}"))

        name = body.get("name")
        description = body.get("description")
        image = body.get("image")
        price = body.get("price")

        create_product(cursor, name, description, image, price)

        return {"statusCode": 201, "body": json.dumps({"message": "Product Created"})}

    except Exception as error:
        context.serverless_sdk.capture_exception(error)
        return {"statusCode": 500, "body": json.dumps({"message": str(error)})}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
