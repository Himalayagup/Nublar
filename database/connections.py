import sqlite3

def get_connection():
    conn = sqlite3.connect("nublar_base.db")
    return conn