import sqlite3

def get_connection():
    conn = sqlite3.connect("nublar_base_db.db")
    return conn