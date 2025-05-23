import json
import os
from . import status_codes
import inspect
from core.template import render_template

class Response:
    def __init__(self, content, status=status_codes.HTTP_200_OK, content_type="text/plain", cookies=None):
        self.content = content
        self.status = status
        self.content_type = content_type
        self.cookies = cookies if cookies else []

    def as_bytes(self):
        if isinstance(self.content, str):
            return self.content.encode()
        return self.content

    def add_cookie(self, cookie_header):
        self.cookies.append(cookie_header)

def json_response(data: dict, status=status_codes.HTTP_200_OK):
    body = json.dumps(data)
    return Response(body, status=status, content_type="application/json")

def html_response(html: str, status=status_codes.HTTP_200_OK):
    return Response(html, status=status, content_type="text/html")

def template_response(template: str, context={}, status=status_codes.HTTP_200_OK):
    caller_frame = inspect.stack()[1]  # [1] gives the caller's frame
    caller_file_path = caller_frame.filename
    caller_directory_path = os.path.dirname(caller_file_path)
    html_rendered = render_template(template, context, caller_directory_path)
    return Response(html_rendered, status=status, content_type="text/html")

def text_response(text: str, status=status_codes.HTTP_200_OK):
    return Response(text, status=status, content_type="text/plain")
