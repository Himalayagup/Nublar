import os
import importlib
from database.model_utils import get_model_schema, compare_schemas, write_migration

def run(apps):
    if isinstance(apps, str):
        apps = [apps]

    for app_name in apps:
        try:
            models_module = importlib.import_module(f"{app_name}.models")
        except ModuleNotFoundError:
            print(f"No models.py in {app_name}")
            continue

        model_classes = [
            cls for name, cls in models_module.__dict__.items()
            if isinstance(cls, type) and hasattr(cls, "_meta")
        ]

        if not model_classes:
            print(f"No models found in {app_name}")
            continue

        write_migration(app_name, model_classes)
