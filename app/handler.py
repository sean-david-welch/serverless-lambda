import os
import json
import psycopg2

from typing import Any, Dict
from dotenv import load_dotenv
from app.queries import create_product, fetch_products, update_product, remove_product

load_dotenv()

connection_params = {
    "host": os.environ["PGHOST"],
    "dbname": os.environ["PGDATABASE"],
    "user": os.environ["PGUSER"],
    "password": os.environ["PGPASSWORD"],
    "port": os.environ["PGPORT"],
}


def get_products(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                result = fetch_products(cursor)

                return {
                    "statusCode": 200,
                    "body": json.dumps({"message": "Query executed", "data": result}),
                }

    except Exception as error:
        context.serverless_sdk.capture_exception(error)
        return {"statusCode": 500, "body": json.dumps({"message": str(error)})}


def post_product(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                body = json.loads(event.get("body", "{}"))

                name = body.get("name")
                description = body.get("description")
                image = body.get("image")
                price = body.get("price")

                product_id = create_product(cursor, name, description, image, price)

                return {
                    "statusCode": 201,
                    "body": json.dumps(
                        {
                            "message": "Product Created",
                            "product": {
                                "id": str(product_id),
                                "name": name,
                                "description": description,
                                "image": image,
                                "price": price,
                            },
                        }
                    ),
                }

    except Exception as error:
        context.serverless_sdk.capture_exception(error)
        return {"statusCode": 500, "body": json.dumps({"message": str(error)})}


def put_product(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                id = event["pathParameters"]["id"]

                body = json.loads(event.get("body", "{}"))

                name = body.get("name")
                description = body.get("description")
                image = body.get("image")
                price = body.get("price")

                update_product(cursor, id, name, description, image, price)

                return {
                    "statusCode": 200,
                    "body": json.dumps(
                        {
                            "message": "Product Updated",
                            "product": {
                                "id": str(id),
                                "name": name,
                                "description": description,
                                "image": image,
                                "price": price,
                            },
                        }
                    ),
                }

    except Exception as error:
        context.serverless_sdk.capture_exception(error)
        return {"statusCode": 500, "body": json.dumps({"message": str(error)})}


def delete_product(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                id = event["pathParameters"]["id"]

                remove_product(cursor, id)

                return {
                    "statusCode": 204,
                    "body": json.dumps(
                        {"message": "Product Deleted", "product_id": id}
                    ),
                }

    except Exception as error:
        context.serverless_sdk.capture_exception(error)
        return {"statusCode": 500, "body": json.dumps({"message": str(error)})}
