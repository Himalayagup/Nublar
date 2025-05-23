from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
from mimetypes import MimeTypes
import os
import json
import traceback

from core.path import ALL_PATHS
from response.main import Response, status_codes
import settings

DEBUG_CODE = getattr(settings, 'DEBUG_CODE', True)

class RequestHandler(BaseHTTPRequestHandler):

    def handle_request(self):
        method = self.command.upper()
        path = self.path
        static_folder = RequestHandler.static_folder
        if static_folder.startswith("/"):
            static_folder = static_folder[1:]
        if static_folder.endswith("/"):
            static_folder = static_folder[:-1]
        try:
            if path.startswith(f"/{static_folder}/"):
                file_path = os.path.join(os.getcwd(), unquote(path.lstrip('/')))
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    mime = MimeTypes()
                    # Get MIME type from file extension
                    content_type, _ = mime.guess_type(file_path)

                    if content_type is None:
                        content_type = 'application/octet-stream'
                    # Send a 200 response, headers, and the file content
                    self.send_response(status_codes.HTTP_200_OK)
                    self.send_header("Content-Type", content_type)
                    self.end_headers()

                    with open(file_path, "rb") as f:
                        self.wfile.write(f.read())
                    return

            for route in ALL_PATHS:
                match = route["regex"].match(path)
                if match:
                    if method not in route["methods"]:
                        self.send_response(status_codes.HTTP_405_METHOD_NOT_ALLOWED)
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
                                self.send_response(status_codes.HTTP_400_BAD_REQUEST)
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
                        self.send_response(status_codes.HTTP_200_OK)
                        self.send_header("Content-Type", "text/plain")
                        self.end_headers()
                        self.wfile.write(response.encode())
                    else:
                        self.send_response(status_codes.HTTP_200_OK)
                        self.end_headers()
                        self.wfile.write(response)
                    return

            self.send_response(status_codes.HTTP_404_NOT_FOUND)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
        except Exception as e:
            self.handle_error(e)
    def handle_error(self, exception):
        """Handle errors and return a 500 Internal Server Error response."""
        self.send_response(status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        
        if DEBUG_CODE:
            # Show full error details if DEBUG_CODE is True
            error_message = f"Internal Server Error\n\n{str(exception)}\n\n{traceback.format_exc()}"
            self.wfile.write(error_message.encode())
        else:
            # Show a generic error message if DEBUG_CODE is False
            self.wfile.write(b"Internal Server Error")
    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()
    def do_PUT(self): self.handle_request()
    def do_PATCH(self): self.handle_request()
    def do_DELETE(self): self.handle_request()

    def log_message(self, format, *args): return
