# app.py
from nublar.path import path  # Import the 'path' decorator for defining URL routes
from response.http_response import json_response, text_response  # Import response functions

# Define the base path for the API, e.g., "/v1"
BASE_PATH = "/v1/"  # It's recommended to avoid starting or ending the path with a slash ('/')

# Route for submitting data via a POST request to "/v1/post"
@path("/post", methods=["POST"])  # Accepts only POST method
def submit_data(req, method, data):
    """
    Handle POST requests to the '/v1/post' endpoint.
    - Retrieves the 'name' field from the request body (default: 'Anonymous' if not provided).
    - Returns a simple text response with the submitted name.
    """
    name = data.get("name") or "Anonymous"  # Default to "Anonymous" if no name is provided
    if isinstance(name, list):  # If the name is a list (e.g., from form encoding), take the first item
        name = name[0]
    return text_response(f"Post Received name: {name}")  # Return the name in the response text

# Route for handling both GET and POST requests to "/v1/json"
@path("/json", methods=["GET", "POST"], active=False)  # Can handle both GET and POST methods (but route is inactive)
def api_data(req, method, data=None):
    """
    Handle GET and POST requests to the '/v1/json' endpoint.
    - Returns a JSON response for both methods.
    - The content of the response differs depending on the HTTP method (GET or POST).
    """
    if method == "POST":
        # If the method is POST, return a message specific to POST requests
        return json_response({"message": "This is a POST JSON Response."}, status=200)
    # If the method is GET (default), return a message specific to GET requests
    return json_response({"message": "This is a GET JSON Response."}, status=200)
