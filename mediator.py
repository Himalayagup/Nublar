# mediator.py

import sys
from nublar.commands import makemigrations, migrate
from settings import INSTALLED_APPS

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: mediator.py [makemigrations|migrate] [app_name?]")
        return

    command = args[0]
    if command == "makemigrations":
        app = args[1] if len(args) > 1 else None
        makemigrations.run(app or INSTALLED_APPS)
    elif command == "migrate":
        migrate.run(INSTALLED_APPS)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
