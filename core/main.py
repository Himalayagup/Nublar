from http.server import HTTPServer
from .request_handler import RequestHandler

class CoreHTTPServer:
    def __init__(self, host='localhost', port=4000):
        self.server_address = (host, port)
        self.httpd = HTTPServer(self.server_address, RequestHandler)

    def start(self):
        host, port = self.server_address
        print(f"Starting server at http://{host}:{port}")
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            self.httpd.server_close()
