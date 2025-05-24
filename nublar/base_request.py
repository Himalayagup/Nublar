# request.py
class Request:
    def __init__(self, *, method, path, headers, query, body=None, cookies=None, path_params=None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.query = query or {}
        self.body = body or {}
        self.cookies = cookies or {}
        self.path_params = path_params or {}