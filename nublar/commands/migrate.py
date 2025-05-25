import os
import importlib

def run(apps):
    if isinstance(apps, str):
        apps = [apps]

    for app in apps:
        migrations_dir = os.path.join(app, "migrations")
        if not os.path.exists(migrations_dir):
            continue

        migration_files = sorted([
            f for f in os.listdir(migrations_dir)
            if f.endswith(".py") and not f.startswith("__")
        ])

        for fname in migration_files:
            modname = f"{app}.migrations.{fname[:-3]}"
            module = importlib.import_module(modname)
            if hasattr(module, "run"):
                print(f"Applying {modname}...")
                module.run()
