# db/connection.py
import sqlite3

def get_connection():
    conn = sqlite3.connect("nublar_one.db")
    return conn

def ensure_migration_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );
    """)
    conn.commit()
    conn.close()
