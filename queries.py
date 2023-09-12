def fetch_products(cursor):
    cursor.execute('SELECT * FROM "Product"')
    return cursor.fetchall()
