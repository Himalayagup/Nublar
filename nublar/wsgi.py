import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your application components
from nublar.http_server import CoreHTTPServer
import settings
import app
import nublar.app

# Create a WSGI application
def application(environ, start_response):
    """
    WSGI application entry point.
    This function adapts your CoreHTTPServer to the WSGI interface.
    """
    # Create a request handler instance
    handler = CoreHTTPServer(host=settings.HOST, port=settings.PORT)
    
    # Process the request using your existing handler
    try:
        # Convert WSGI environ to your request format
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        query_string = environ.get('QUERY_STRING', '')
        headers = {k.replace('HTTP_', '').replace('_', '-').lower(): v 
                  for k, v in environ.items() if k.startswith('HTTP_')}
        
        # Get request body if present
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        
        # Process the request using your existing handler
        response = handler.handle_request(method, path, query_string, headers, body)
        
        # Send response
        status = f"{response.status} {response.status_text}"
        response_headers = [(k, v) for k, v in response.headers.items()]
        start_response(status, response_headers)
        
        return [response.body]
        
    except Exception as e:
        # Handle errors
        status = '500 Internal Server Error'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return [b'Internal Server Error']

# For server
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 4000, application)
    print("Serving on http://127.0.0.1:4000")
    server.serve_forever() 