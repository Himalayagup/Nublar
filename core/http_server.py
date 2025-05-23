from http.server import HTTPServer
from .request_handler import RequestHandler
import settings
from .utils import removing_slashes

HOST = getattr(settings, 'HOST', '127.0.0.1')
PORT = getattr(settings, 'PORT', 4000)
PORT = int(PORT) if isinstance(PORT, str) else PORT
STATIC_FOLDER = getattr(settings, 'STATIC_FOLDER', 'static')
if STATIC_FOLDER:
    STATIC_FOLDER = removing_slashes(STATIC_FOLDER)
else:
    STATIC_FOLDER = "static"

class CoreHTTPServer:
    def __init__(self, host=HOST, port=PORT, static_folder=STATIC_FOLDER):
        self.server_address = (host, port)
        self.static_folder = static_folder
        self.httpd = HTTPServer(self.server_address, RequestHandler)

    def start(self):
        host, port = self.server_address
        print(f"Starting server at http://{host}:{port}")

        # Set the static folder for the request handler
        RequestHandler.static_folder = self.static_folder

        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            self.httpd.server_close()

