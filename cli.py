#!/usr/bin/env python
# cli.py – CLI entry point (using argparse) for running the server and scaffolding a new app

import argparse
import os
import shutil
import sys

# Import the necessary components for runserver (from run.py)
from nublar.http_server import CoreHTTPServer
import settings

# --- CLI Parser ---
parser = argparse.ArgumentParser(description="Nublar CLI (manage.py-like) for running the server and scaffolding a new app.")
subparsers = parser.add_subparsers(dest="command", help="Command to run (runserver or startapp)")

# --- runserver command ---
runserver_parser = subparsers.add_parser("runserver", help="Start the HTTP server (like run.py).")
runserver_parser.add_argument("--host", type=str, default=settings.HOST, help="Host (default: from settings, or 127.0.0.1)")
runserver_parser.add_argument("--port", type=int, default=settings.PORT, help="Port (default: from settings, or 4000)")

# --- startapp command ---
startapp_parser = subparsers.add_parser("startapp", help="Scaffold a new app (like example_app).")
startapp_parser.add_argument("app_name", type=str, help="Name of the new app (e.g., my_new_app)")

# --- Helper function to scaffold a new app ---
def scaffold_app(app_name):
    """Scaffold a new app (folder) with pre-coded files (pages.py, urls.py, __init__.py, and a templates folder with a sample template)."""
    if os.path.exists(app_name):
        print(f"Error: Folder '{app_name}' already exists. Aborting.")
        sys.exit(1)
    os.makedirs(app_name, exist_ok=True)
    os.makedirs(os.path.join(app_name, "templates"), exist_ok=True)

    # Create __init__.py (empty file)
    with open(os.path.join(app_name, "__init__.py"), "w") as f:
         f.write("# __init__.py for new app\n")

    # Create pages.py (copy from example_app/pages.py)
    with open(os.path.join("example_app", "pages.py"), "r") as f_in:
         pages_content = f_in.read()
    with open(os.path.join(app_name, "pages.py"), "w") as f_out:
         f_out.write(pages_content)

    # Create urls.py (copy from example_app/urls.py)
    with open(os.path.join("example_app", "urls.py"), "r") as f_in:
         urls_content = f_in.read()
    with open(os.path.join(app_name, "urls.py"), "w") as f_out:
         f_out.write(urls_content)

    # Create a sample template (copy example_app/templates/about.html)
    if os.path.exists(os.path.join("example_app", "templates", "about.html")):
         with open(os.path.join("example_app", "templates", "about.html"), "r") as f_in:
              tmpl_content = f_in.read()
         with open(os.path.join(app_name, "templates", "about.html"), "w") as f_out:
              f_out.write(tmpl_content)
    else:
         # Fallback: create a minimal about.html if example template is missing
         with open(os.path.join(app_name, "templates", "about.html"), "w") as f:
              f.write("<html><body><h1>About</h1><p>This is a scaffolded about page.</p></body></html>")

    print(f"New app '{app_name}' scaffolded successfully.")


# --- CLI entry point ---
if __name__ == "__main__":
    args = parser.parse_args()
    if args.command == "runserver":
         host = args.host or settings.HOST
         port = args.port or settings.PORT
         print(f"Starting server at http://{host}:{port} (press Ctrl+C to stop)")
         server = CoreHTTPServer(host=host, port=port)
         server.start()
    elif args.command == "startapp":
         scaffold_app(args.app_name)
    else:
         parser.print_help()
