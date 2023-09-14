import os
import json
import psycopg2

from typing import Any, Dict
from dotenv import load_dotenv
from app.queries import create_table

load_dotenv()

connection_params = {
    "host": os.environ["PGHOST"],
    "dbname": os.environ["PGDATABASE"],
    "user": os.environ["PGUSER"],
    "password": os.environ["PGPASSWORD"],
    "port": os.environ["PGPORT"],
}


def post_table(event: Dict[Any, Any], context: Any) -> Dict[str, Any]:
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                body = json.loads(event.get("body", "{}"))
                columns = body.get("columns", {})
                table_name = body.get("table_name", "")

                if columns and table_name:
                    create_table(cursor, table_name, columns)

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Table created", "Table": columns}),
        }

    except Exception as error:
        context.serverless_sdk.capture_exception(error)
        return {"statusCode": 500, "body": json.dumps({"message": str(error)})}
