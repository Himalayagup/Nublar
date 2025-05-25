import json
import os
from . import status_codes  # Import status codes for HTTP responses
import inspect
from nublar.template import render_template  # Function to render templates

class Response:
    """
    Represents an HTTP Response.
    Includes content, status code, content type, and optional cookies.
    """
    def __init__(self, content, status=status_codes.HTTP_200_OK, content_type="text/plain", cookies=None):
        """
        Initializes a new Response object.

        :param content: The content of the response (e.g., text, HTML, JSON)
        :param status: The HTTP status code (default: HTTP_200_OK)
        :param content_type: The content type of the response (default: "text/plain")
        :param cookies: Optional list of cookies to be included in the response
        """
        self.content = content  # The body/content of the response
        self.status = status  # HTTP status code of the response
        self.content_type = content_type  # Content type (e.g., text, HTML, JSON)
        self.cookies = cookies if cookies else []  # List of cookies, defaults to empty list if not provided

    def as_bytes(self):
        """
        Convert the content into bytes to be sent over HTTP.

        :return: Content as bytes (encoded string or raw content)
        """
        if isinstance(self.content, str):
            return self.content.encode()  # Convert string content to bytes
        return self.content  # If already in bytes, return as-is

    def add_cookie(self, cookie_header):
        """
        Adds a cookie to the response.

        :param cookie_header: The cookie header string to be added to the response
        """
        self.cookies.append(cookie_header)  # Appends the cookie to the response's cookies list

# Helper function to create a JSON response
def json_response(data: dict, status=status_codes.HTTP_200_OK):
    """
    Create a JSON response.

    :param data: Dictionary containing data to be returned as JSON
    :param status: HTTP status code (default: HTTP_200_OK)
    :return: Response object with JSON content
    """
    body = json.dumps(data)  # Convert dictionary to JSON string
    return Response(body, status=status, content_type="application/json")  # Return Response with JSON content

# Helper function to create an HTML response
def html_response(html: str, status=status_codes.HTTP_200_OK):
    """
    Create an HTML response.

    :param html: HTML content to be returned in the response
    :param status: HTTP status code (default: HTTP_200_OK)
    :return: Response object with HTML content
    """
    return Response(html, status=status, content_type="text/html")  # Return Response with HTML content

# Helper function to create a response rendered from a template
def template_response(template: str, context={}, status=status_codes.HTTP_200_OK):
    """
    Create a response rendered from a template.

    :param template: The template file name to render
    :param context: The context data to pass to the template for rendering
    :param status: HTTP status code (default: HTTP_200_OK)
    :return: Response object with the rendered HTML content
    """
    caller_frame = inspect.stack()[1]  # Get the calling stack frame (caller)
    caller_file_path = caller_frame.filename  # Get the file path of the caller
    caller_directory_path = os.path.dirname(caller_file_path)  # Get the directory of the caller's file
    html_rendered = render_template(template, context, caller_directory_path)  # Render the template with context
    return Response(html_rendered, status=status, content_type="text/html")  # Return Response with the rendered HTML content

# Helper function to create a plain text response
def text_response(text: str, status=status_codes.HTTP_200_OK):
    """
    Create a plain text response.

    :param text: Text content to be returned in the response
    :param status: HTTP status code (default: HTTP_200_OK)
    :return: Response object with plain text content
    """
    return Response(text, status=status, content_type="text/plain")  # Return Response with plain text content
