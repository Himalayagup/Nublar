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
    import os
    from datetime import datetime

    migrations_dir = os.path.join(app_name, "migrations")
    os.makedirs(migrations_dir, exist_ok=True)

    init_path = os.path.join(migrations_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w"):
            pass

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"{ts}_auto.py"
    path = os.path.join(migrations_dir, fname)

    with open(path, "w", encoding="utf-8") as f:
        f.write("from database.connections import get_connection\n\n")
        f.write("def run():\n")

        # Add at least one indented line to avoid indentation errors
        if not model_classes:
            f.write("    pass\n")  # if no models, put pass to avoid syntax error

        for cls in model_classes:
            sql = generate_create_sql(cls)
            # Indent SQL properly by prefixing each line with 8 spaces
            sql_lines = sql.splitlines()
            sql_indented = "\n        ".join(sql_lines)  # 8 spaces for inside triple quotes
            f.write(f'    get_connection().execute("""\n        {sql_indented}\n    """)\n')
            f.write(f'    print("Created table: {cls.__name__}")\n')

    print(f"Created migration: {path}")

