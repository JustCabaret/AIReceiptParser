import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'receipts.db')

def get_db_connection():
    """Returns a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # This allows accessing columns by name
    return connection

def init_db():
    """Initializes the database tables if they don't exist."""
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total INTEGER NOT NULL,
            source TEXT NOT NULL,
            parsed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipt_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price INTEGER NOT NULL,
            category TEXT DEFAULT NULL,
            FOREIGN KEY (receipt_id) REFERENCES receipts(id)
        )
    ''')

    connection.commit()
    connection.close()

def insert_receipt(data):
    """Inserts a receipt and its items into the database."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert the receipt
    query_receipt = "INSERT INTO receipts (total, source) VALUES (?, ?)"
    cursor.execute(query_receipt, (data["total"], data.get("store", "Unknown")))
    receipt_id = cursor.lastrowid

    # Insert the items
    query_item = """
    INSERT INTO receipt_items (receipt_id, product, quantity, price, category)
    VALUES (?, ?, ?, ?, ?)
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
    connection.close()

    return receipt_id

def fetch_all_receipts():
    """
    Fetches all receipts from the database with their main details.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT id, total, source AS store FROM receipts"
    cursor.execute(query)
    results = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return results

def fetch_receipt_details(receipt_id):
    """
    Fetches all items associated with a specific receipt.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT product, quantity, price, category
    FROM receipt_items
    WHERE receipt_id = ?
    """
    cursor.execute(query, (receipt_id,))
    results = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return {"receipt_id": receipt_id, "items": results}