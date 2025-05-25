import os
import json
from datetime import datetime
from pprint import pformat
from .connections import get_connection

def get_model_schema(model_cls):
    fields = {}
    for name, field in model_cls._meta["fields"].items():
        fields[name] = {"type": field.type, "primary_key": field.primary_key}
    return fields

def compare_schemas(old, new):
    ops = []
    for field in new.keys() - old.keys():
        ops.append(("AddField", field, new[field]))
    for field in old.keys() - new.keys():
        ops.append(("RemoveField", field))
    for field in new.keys() & old.keys():
        if old[field] != new[field]:
            ops.append(("AlterField", field, new[field]))
    return ops

def write_migration(app_name, model_classes):
    migrations_dir = os.path.join(app_name, "migrations")
    os.makedirs(migrations_dir, exist_ok=True)
    init_file = os.path.join(migrations_dir, "__init__.py")
    if not os.path.exists(init_file):
        open(init_file, "w").close()

    prev_schema = {}
    migration_files = sorted([
        f for f in os.listdir(migrations_dir)
        if f.endswith(".py") and not f.startswith("__")
    ])
    if migration_files:
        last_file = os.path.join(migrations_dir, migration_files[-1])
        with open(last_file) as f:
            code = compile(f.read(), last_file, 'exec')
            ns = {}
            exec(code, ns)
            prev_schema = ns.get("schema", {})

    new_schema = {}
    ops_by_model = {}
    for model in model_classes:
        name = model.__name__
        schema = get_model_schema(model)
        new_schema[name] = schema
        if name not in prev_schema:
            # New model, generate CREATE TABLE
            ops_by_model[name] = [("CreateModel", schema)]
        else:
            ops = compare_schemas(prev_schema[name], schema)
            if ops:
                ops_by_model[name] = ops

    if not ops_by_model:
        print(f"No changes in {app_name}")
        return

    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"{ts}_auto.py"
    path = os.path.join(migrations_dir, fname)

    with open(path, "w") as f:
        f.write("from database.connections import get_connection\n")
        f.write("def run():\n")
        for model, ops in ops_by_model.items():
            table = model.lower()
            for op in ops:
                if op[0] == "AddField":
                    f.write(f"    get_connection().execute(\"ALTER TABLE {table} ADD COLUMN {op[1]} {op[2]['type']}\")\n")
                elif op[0] == "AlterField":
                    f.write(f"    print('Manual migration needed to alter {op[1]} in {table}')\n")
                elif op[0] == "RemoveField":
                    f.write(f"    print('Manual migration needed to remove {op[1]} in {table}')\n")
        f.write(f"\nschema = {pformat(new_schema)}\n")

    print(f"Created migration: {fname}")
