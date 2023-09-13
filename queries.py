from uuid import uuid4


def fetch_products(cursor):
    cursor.execute('SELECT * FROM "product"')
    return cursor.fetchall()


def create_product(cursor, name, description, image, price):
    id = uuid4()
    query = """
            INSERT INTO "product" (id, name, description, image, price)
            VALUES (%s, %s, %s, %s, %s)
            """
    cursor.execute(query, (str(id), name, description, image, price))
    cursor.connection.commit()

    return id
