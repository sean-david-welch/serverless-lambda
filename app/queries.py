from uuid import uuid4
from psycopg2 import sql


# Product CRUD
def create_product(cursor, name, description, image, price):
    id = uuid4()

    query = sql.SQL(
        """
        INSERT INTO "product" (id, name, description, image, price)
        VALUES (%s, %s, %s, %s, %s)
        """
    )

    cursor.execute(query, (str(id), name, description, image, price))
    cursor.connection.commit()

    return id


def fetch_products(cursor):
    query = sql.SQL(
        """
        SELECT * FROM "product"
        """
    )

    cursor.execute(query)

    return cursor.fetchall()


def update_product(cursor, id, name, description, image, price):
    query = sql.SQL(
        """
        UPDATE "product"
        SET name = %s, description = %s, image = %s, price = %s
        WHERE id = %s
        """
    )

    cursor.execute(query, (name, description, image, price, str(id)))


def delete_product(cursor, id):
    query = sql.SQL(
        """
        DELETE FROM "product" WHERE id = %s
        """
    )

    cursor.execute(query, (str(id)))
    cursor.connnection.commit()
