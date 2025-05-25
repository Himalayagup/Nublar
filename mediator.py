import os
import sys
import importlib.util
from database.connections import get_connection, ensure_migration_table
from database.generate import makemigrations

APPS = ['example_app']  # Add other app names here

def load_models_from_app(app):
    all_models = []
    model_path = os.path.join(app, "models.py")
    if os.path.exists(model_path):
        spec = importlib.util.spec_from_file_location(f"{app}.models", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr in dir(module):
            cls = getattr(module, attr)
            if hasattr(cls, "_meta"):
                all_models.append(cls)
    return all_models

def get_applied_migrations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM migrations")
    return {row[0] for row in cursor.fetchall()}

def mark_as_applied(name):
    conn = get_connection()
    conn.execute("INSERT INTO migrations (name) VALUES (?)", (name,))
    conn.commit()

def migrate():
    ensure_migration_table()
    applied = get_applied_migrations()
    for app in APPS:
        migration_dir = os.path.join(app, "migrations")
        if not os.path.exists(migration_dir):
            continue
        for fname in sorted(os.listdir(migration_dir)):
            if not fname.endswith(".py") or fname.startswith("__"):
                continue
            migration_name = f"{app}.{fname}"
            if migration_name in applied:
                continue
            path = os.path.join(migration_dir, fname)
            spec = importlib.util.spec_from_file_location(f"{app}.migration", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.run()
            mark_as_applied(migration_name)
            print(f"Applied: {migration_name}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd == "makemigrations":
        for app in APPS:
            models = load_models_from_app(app)
            if models:
                makemigrations(app, models)
    elif cmd == "migrate":
        migrate()
    else:
        print("Usage: python manage.py [makemigrations|migrate]")
