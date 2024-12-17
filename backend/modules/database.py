import mysql.connector

def get_db_connection():
    """Returns a connection to the database."""
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Update as needed
        password="",  # Update as needed
        database="receiptparserdb"
    )

def insert_receipt(data):
    """Inserts a receipt and its items into the database."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert the receipt
    query_receipt = "INSERT INTO receipts (total, source) VALUES (%s, %s)"
    cursor.execute(query_receipt, (data["total"], data.get("store", "Unknown")))
    receipt_id = cursor.lastrowid

    # Insert the items
    query_item = """
    INSERT INTO receipt_items (receipt_id, product, quantity, price, category)
    VALUES (%s, %s, %s, %s, %s)
    """
    for item in data["items"]:
        cursor.execute(query_item, (
            receipt_id,
            item["product"],
            item["quantity"],
            item["price"],
            item.get("type", "Unknown")
        ))

    connection.commit()
    cursor.close()
    connection.close()

    return receipt_id

def fetch_all_receipts():
    """
    Fetches all receipts from the database with their main details.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT id, total, source AS store FROM receipts"
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

def fetch_receipt_details(receipt_id):
    """
    Fetches all items associated with a specific receipt.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT product, quantity, price, category
    FROM receipt_items
    WHERE receipt_id = %s
    """
    cursor.execute(query, (receipt_id,))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return {"receipt_id": receipt_id, "items": results}