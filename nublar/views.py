# core/views.py
from response.http_response import Response
from response import status_codes
from response.http_response import text_response, json_response

# core/views.py
class BaseView:
    def dispatch(self, request, **kwargs):
        """Dispatch method to handle different HTTP methods."""
        method = request.command.upper()  # Get the HTTP method
        handler = getattr(self, method.lower(), self.http_method_not_allowed)
        return handler(request, **kwargs)

    def http_method_not_allowed(self, request, **kwargs):
        """Handle unsupported HTTP methods."""
        return text_response("Method Not Allowed", status=status_codes.HTTP_405_METHOD_NOT_ALLOWED)

    def get(self, request, **kwargs):
        """Handle GET requests. To be overridden by subclasses."""
        raise NotImplementedError

    def post(self, request, **kwargs):
        """Handle POST requests. To be overridden by subclasses."""
        raise NotImplementedError

    def put(self, request, **kwargs):
        """Handle PUT requests. To be overridden by subclasses."""
        raise NotImplementedError

