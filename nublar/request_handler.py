from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
from mimetypes import MimeTypes
import os
import json
import traceback

from nublar.path import ALL_PATHS  # List of all registered routes
from response.http_response import Response  # Response class to create HTTP responses
from response import status_codes  # HTTP status codes
import settings  # Settings module for configuration
from nublar.utils import removing_slashes  # Utility to clean up slashes in paths

DEBUG_CODE = getattr(settings, 'DEBUG_CODE', True)  # Set debug mode from settings
if DEBUG_CODE in [None, False] or isinstance(DEBUG_CODE, str):
    DEBUG_CODE = True  # Default to True if not set in settings or not set properly

class RequestHandler(BaseHTTPRequestHandler):
    """
    Custom request handler to handle HTTP requests, match them to registered routes,
    serve static files, and generate HTTP responses.
    """

    def handle_request(self):
        """
        This method processes the incoming HTTP request, finds the matching route,
        handles cookies, parses body data (for POST, PUT, PATCH), and sends the response.
        """

        method = self.command.upper()  # The HTTP method (GET, POST, etc.)
        path = self.path  # The request path (URL)
        static_folder = removing_slashes(RequestHandler.static_folder)  # Static folder path from settings

        # Cookie handling: Get cookies from the request
        cookies = self.headers.get('Cookie', '')
        self.cookies = parse_qs(cookies.replace('; ', '&'))  # Parse cookies into a dictionary


        try:
            # Check if the path is for a static file
            if path.startswith(f"/{static_folder}/"):
                file_path = os.path.join(os.getcwd(), unquote(path.lstrip('/')))    # Get the absolute path
                if os.path.exists(file_path) and os.path.isfile(file_path):     # Check if the file exists
                    mime = MimeTypes()  # Create MimeTypes object to guess MIME type
                    content_type, _ = mime.guess_type(file_path) # Get the MIME type of the file

                    # If MIME type is not found, set default to 'application/octet-stream'
                    if content_type is None:
                        content_type = 'application/octet-stream'

                    # Send a 200 response, headers, and the file content
                    self.send_response(status_codes.HTTP_200_OK)
                    self.send_header("Content-Type", content_type)
                    self.end_headers()

                    with open(file_path, "rb") as f:
                        self.wfile.write(f.read())  # Write the file content to the response
                    return

            # If path is not for a static file, match against registered routes
            for route in ALL_PATHS:
                match = route["regex"].match(path)  # Check if path matches any route's regex
                if match:
                    # If method is not allowed, return 405 Method Not Allowed
                    if method not in route["methods"]:
                        self.send_response(status_codes.HTTP_405_METHOD_NOT_ALLOWED)
                        self.end_headers()
                        self.wfile.write(b"405 Method Not Allowed")
                        return

                    kwargs = match.groupdict()   # Extract parameters from the path

                    # Handle POST/PUT/PATCH data
                    data = {}
                    if method in ("POST", "PUT", "PATCH"):
                        length = int(self.headers.get("Content-Length", 0))
                        raw = self.rfile.read(length).decode()  # Read the request body

                        content_type = self.headers.get("Content-Type", "")

                        # Parse JSON data
                        if "application/json" in content_type:
                            try:
                                data = json.loads(raw)
                            except json.JSONDecodeError:
                                self.send_response(status_codes.HTTP_400_BAD_REQUEST)
                                self.end_headers()
                                self.wfile.write(b"Invalid JSON")
                                return

                        # Parse form-encoded data
                        elif "application/x-www-form-urlencoded" in content_type:
                            data = parse_qs(raw)
                        else:
                            data = {"raw": raw}  # Default to raw data

                    # Prepare the arguments to pass to the route handler function
                    call_args = {
                        "req": self,    # Pass the request object to the handler
                        "method": method,
                        **kwargs,   # Additional parameters from the URL path
                    }

                    if method in ("POST", "PUT", "PATCH", "DELETE"):
                        call_args["data"] = data    # Include the data for methods that have a body

                    # Call the route handler function and get the response
                    response = route["func"](**call_args)

                    # Handle the response depending on its type (Response object, string, or raw content)
                    if isinstance(response, Response):
                        # If the response is a Response object, send it back with headers and body
                        self.send_response(response.status)
                        self.send_header("Content-Type", response.content_type)
                        if response.cookies:
                            for cookie in response.cookies:
                                self.send_header("Set-Cookie", cookie)   # Set cookies in headers
                        self.end_headers()
                        self.wfile.write(response.as_bytes())   # Send response body
                    elif isinstance(response, str):
                        # If the response is a string, send it as plain text
                        self.send_response(status_codes.HTTP_200_OK)
                        self.send_header("Content-Type", "text/plain")
                        self.end_headers()
                        self.wfile.write(response.encode())  # Send string response
                    else:
                        # If the response is raw content (e.g., bytes), send it directly
                        self.send_response(status_codes.HTTP_200_OK)
                        self.end_headers()
                        self.wfile.write(response)  # Send raw response
                    return

            # If no route matches, send a 404 Not Found response
            self.send_response(status_codes.HTTP_404_NOT_FOUND)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
        except Exception as e:
            # Handle any unexpected errors and send a 500 Internal Server Error response
            self.handle_error(e)

    def handle_error(self, exception):
        """
        Handle errors and return a 500 Internal Server Error response.
        If DEBUG_CODE is True, show full error details; otherwise, show a generic error message.
        """
        self.send_response(status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        if DEBUG_CODE:
            # Show detailed error message and stack trace in debug mode
            error_message = f"Internal Server Error\n\n{str(exception)}\n\n{traceback.format_exc()}"
            self.wfile.write(error_message.encode())
        else:
            # Show a generic error message if DEBUG_CODE is False
            self.wfile.write(b"Internal Server Error")

    # HTTP methods (GET, POST, PUT, PATCH, DELETE) that call handle_request
    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()
    def do_PUT(self): self.handle_request()
    def do_PATCH(self): self.handle_request()
    def do_DELETE(self): self.handle_request()

    # Disable logging of HTTP requests (overrides BaseHTTPRequestHandler's default behavior)
    def log_message(self, format, *args): return
