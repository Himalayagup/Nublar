import json
from . import status_codes

class Response:
    def __init__(self, content, status=200, content_type="text/plain"):
        self.content = content
        self.status = status
        self.content_type = content_type

    def as_bytes(self):
        if isinstance(self.content, str):
            return self.content.encode()
        return self.content

def json_response(data: dict, status=status_codes.HTTP_200_OK):
    body = json.dumps(data)
    return Response(body, status=status, content_type="application/json")

def html_response(html: str, status=status_codes.HTTP_200_OK):
    return Response(html, status=status, content_type="text/html")

def text_response(text: str, status=status_codes.HTTP_200_OK):
    return Response(text, status=status, content_type="text/plain")
