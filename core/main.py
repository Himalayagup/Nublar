from http.server import HTTPServer
from .request_handler import RequestHandler

class CoreHTTPServer:
    def __init__(self, host='localhost', port=4000, static_folder="static"):
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

