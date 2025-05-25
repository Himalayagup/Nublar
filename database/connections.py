import sqlite3
import settings

db_name = getattr(settings, 'DB_NAME', 'nublar_base_db.db')
if not db_name:
    db_name = 'nublar_base_db.db'

def get_connection():
    conn = sqlite3.connect(db_name)
    return conn