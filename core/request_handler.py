from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

import json


from path import ROUTES
from response.main import Response

class RequestHandler(BaseHTTPRequestHandler):
    def handle_request(self):
        method = self.command.upper()
        path = self.path

        for route in ROUTES:
            match = route["regex"].match(path)
            if match:
                if method not in route["methods"]:
                    self.send_response(405)
                    self.end_headers()
                    self.wfile.write(b"405 Method Not Allowed")
                    return

                kwargs = match.groupdict()

                # Read body for POST/PUT/PATCH
                data = {}
                if method in ("POST", "PUT", "PATCH"):
                    length = int(self.headers.get("Content-Length", 0))
                    raw = self.rfile.read(length).decode()
                    content_type = self.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        try:
                            data = json.loads(raw)
                        except json.JSONDecodeError:
                            self.send_response(400)
                            self.end_headers()
                            self.wfile.write(b"Invalid JSON")
                            return
                    elif "application/x-www-form-urlencoded" in content_type:
                        data = parse_qs(raw)
                    else:
                        data = {"raw": raw}
                call_args = {
                    "req": self,
                    "method": method,
                    **kwargs
                }

                if method in ("POST", "PUT", "PATCH", "DELETE"):
                    call_args["data"] = data

                response = route["func"](**call_args)

                # response = route["func"](self, data=data, **kwargs) if method in ("POST", "PUT", "PATCH") else route["func"](self, **kwargs)
                if isinstance(response, Response):
                    self.send_response(response.status)
                    self.send_header("Content-Type", response.content_type)
                    self.end_headers()
                    self.wfile.write(response.as_bytes())
                elif isinstance(response, str):
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write(response.encode())
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response)
                return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"404 Not Found")

    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()
    def do_PUT(self): self.handle_request()
    def do_PATCH(self): self.handle_request()
    def do_DELETE(self): self.handle_request()

    def log_message(self, format, *args): return
