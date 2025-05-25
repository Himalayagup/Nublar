import os
import importlib

def run(apps):
    app_name_list = []
    if isinstance(apps, str):
        app_name_list = apps.split(",")
    else:
        print("Invalid input: apps should be a string representing the app name. (Multiple names should be separated by commas.)")
        return
    if not app_name_list:
        print("Invalid input: apps should be a string representing the app name. (Multiple names should be separated by commas.)")
        return
    for app in app_name_list:
        app_folder_path = os.path.join(os.getcwd(), app)
        if os.path.exists(app_folder_path):
            print(f"App '{app}' folder already exist in the current directory. Change the app name or remove the existing folder.")
        else:
            os.makedirs(app_folder_path)
            # print(f"App '{app}' folder created successfully.")
            # Create models.py file
            init_file_path = os.path.join(app_folder_path, "__init__.py")
            with open(init_file_path, "w") as init_file:
                pass
            models_file_path = os.path.join(app_folder_path, "models.py")
            with open(models_file_path, "w") as models_file:
                models_file.write("from database.base import Model, IntegerField, CharField\n\n# Define your models here\n")
            pages_file_path = os.path.join(app_folder_path, "pages.py")
            with open(pages_file_path, "w") as pages_file:
                pages_file.write("from nublar.cookies import set_cookie, get_cookie, delete_cookie\nfrom response.http_response import json_response, text_response, html_response, template_response\nfrom nublar.path import path\n\n# Define your page handlers here\n")
            print(f"App '{app}' created successfully with models.py and pages.py files.")
            return
