import sys
from nublar.commands import makemigrations, migrate
from settings import INSTALLED_APPS

# Import your server components
from nublar.http_server import CoreHTTPServer
import settings as app_settings  # to avoid name clash with your local 'settings'

def run_server(host=None, port=None):
    import app
    import nublar.app

    HOST = getattr(app_settings, 'HOST', '127.0.0.1') if not host else host
    if not HOST:
        HOST = '127.0.0.1'

    PORT = getattr(app_settings, 'PORT', 4000) if not port else port
    if not PORT:
        PORT = 4000
    else:
        PORT = int(PORT) if isinstance(PORT, str) else PORT

    server = CoreHTTPServer(host=HOST, port=PORT)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer stopped by user (Ctrl+C). Shutting down...")
        server.stop()  # if you have a stop or cleanup method
    except Exception as e:
        print(f"Server error: {e}")

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: mediator.py [makemigrations|migrate|runserver] [app_name?]")
        return

    command = args[0]
    if command == "makemigrations":
        app = args[1] if len(args) > 1 else None
        makemigrations.run(app or INSTALLED_APPS)
    elif command == "migrate":
        migrate.run(INSTALLED_APPS)
    elif command == "runserver":
        host=None
        port=None
        if len(args) > 1:
            if len(args) ==2:
                if "--host=" in args[1]:
                    host = args[1].split("=")[1]
                if "--port=" in args[1]:
                    port = int(args[1].split("=")[1])
            if len(args) == 3:
                if "--host=" in args[1]:
                    host = args[1].split("=")[1]
                if "--port=" in args[1]:
                    port = int(args[1].split("=")[1])
                if "--host=" in args[2]:
                    host = args[2].split("=")[1]
                if "--port=" in args[2]:
                    port = int(args[2].split("=")[1])
        run_server(host, port)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
