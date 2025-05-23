# run_server.py
from core.main import CoreHTTPServer
import settings
import app
import core.app

HOST = getattr(settings, 'HOST', '127.0.0.1')
if not HOST:
    HOST = '127.0.0.1'
PORT = getattr(settings, 'PORT', 4000)
if not PORT:
    PORT = 4000
else:
    PORT = int(PORT) if isinstance(PORT, str) else PORT

if __name__ == "__main__":
    server = CoreHTTPServer(host=HOST, port=PORT)
    server.start()
