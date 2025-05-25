from database.connections import get_connection

class QuerySet:
    def __init__(self, model):
        self.model = model
        self.table_name = model.__name__.lower()

    def all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name}")
        rows = cur.fetchall()
        conn.close()
        return rows

def objects(model_cls):
    return QuerySet(model_cls)
