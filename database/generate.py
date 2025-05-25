# nublar/generate.py
import os
from datetime import datetime
from database.connections import get_connection

def generate_create_sql(model_cls):
    table = model_cls.__name__.lower()
    fields = []
    for name, field in model_cls._meta['fields'].items():
        line = f"{name} {field.type}"
        if field.primary_key:
            line += " PRIMARY KEY"
        fields.append(line)
    fields_sql = ", ".join(fields)
    return f"CREATE TABLE IF NOT EXISTS {table} ({fields_sql});"

def makemigrations(app_name: str, model_classes):
    migrations_dir = os.path.join(app_name, "migrations")
    os.makedirs(migrations_dir, exist_ok=True)

    # Ensure __init__.py
    init_path = os.path.join(migrations_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w"): pass

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"{ts}_auto.py"
    path = os.path.join(migrations_dir, fname)

    with open(path, "w") as f:
        f.write("from nublar.database.connections import get_connection\n\n")
        f.write("def run():\n")
        for cls in model_classes:
            sql = generate_create_sql(cls)
            f.write(f"    get_connection().execute('''{sql}''')\n")
            f.write(f"    print('Created table: {cls.__name__}')\n")
    print(f"Created migration: {path}")
