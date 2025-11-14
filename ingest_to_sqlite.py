import csv
import sqlite3
from pathlib import Path

DB_NAME = "ecom.db"
CSV_FILES = {
    "users": ("users.csv", ["user_id", "name", "email"]),
    "products": ("products.csv", ["product_id", "name", "category", "price"]),
    "orders": ("orders.csv", ["order_id", "user_id", "order_date"]),
    "order_items": ("order_items.csv", ["item_id", "order_id", "product_id", "quantity"]),
    "payments": ("payments.csv", ["payment_id", "order_id", "amount", "status"]),
}

SCHEMA_STATEMENTS = [
    "DROP TABLE IF EXISTS users;",
    "DROP TABLE IF EXISTS products;",
    "DROP TABLE IF EXISTS orders;",
    "DROP TABLE IF EXISTS order_items;",
    "DROP TABLE IF EXISTS payments;",
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    );
    """,
    """
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """,
    """
    CREATE TABLE order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """,
    """
    CREATE TABLE payments (
        payment_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );
    """,
]

ROOT = Path(__file__).resolve().parent

def read_csv_rows(filename: str, columns: list[str]):
    path = ROOT / filename
    with path.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield [row[column] for column in columns]

def main():
    db_path = ROOT / DB_NAME
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        for statement in SCHEMA_STATEMENTS:
            cursor.executescript(statement)

        insert_statements = {
            "users": "INSERT INTO users (user_id, name, email) VALUES (?, ?, ?);",
            "products": "INSERT INTO products (product_id, name, category, price) VALUES (?, ?, ?, ?);",
            "orders": "INSERT INTO orders (order_id, user_id, order_date) VALUES (?, ?, ?);",
            "order_items": "INSERT INTO order_items (item_id, order_id, product_id, quantity) VALUES (?, ?, ?, ?);",
            "payments": "INSERT INTO payments (payment_id, order_id, amount, status) VALUES (?, ?, ?, ?);",
        }

        for table, (filename, columns) in CSV_FILES.items():
            rows = list(read_csv_rows(filename, columns))
            cursor.executemany(insert_statements[table], rows)

        conn.commit()
        print(f"Data ingested successfully into {db_path}.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
