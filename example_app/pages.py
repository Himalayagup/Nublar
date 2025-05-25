# app.py
from nublar.path import path  # Import the 'path' decorator to define URL routes
from response.http_response import text_response, html_response, template_response  # Import response functions
from response import status_codes  # Import HTTP status codes
from datetime import datetime

# Define route for "/homepage" that responds with a text message
@path("/homepage", methods=["GET"])  # Only allows GET method
def home(req, method, headers):
    """
    Handle the GET request for the homepage.
    Returns a simple text response with a 200 OK status.
    """
    print(f"Headers received: {req.headers}")  # Log headers
    # print(f"Headers received: {headers}")  # Log headers
    return text_response("Welcome to the homepage!", status=status_codes.HTTP_200_OK)

# Define route for "/about" that responds with a text message
@path("/about")  # Default is GET method
def about(req, method, query):
    """
    Handle the request for the about page.
    Returns a simple text response indicating this is the about page.
    """
    print(f"Query parameters received: {query}")  # Log query
    # print(f"Query parameters received: {req.query}")  # Log query
    return text_response("This is the about page.")

# Define route for "/user/<id>" where <id> is a variable part of the URL
@path("/user/<id>")  # Dynamic route to capture user ID
def get_user(req, method, id):
    """
    Handle the request to get user details by user ID.
    Returns a text response with the user ID in the message.
    """
    return text_response(f"User ID is: {id}")

# Define route for "/post/<slug>" to retrieve post by slug
@path("/post/<slug>", methods=["GET"])  # Allows only GET method
def get_post(req, method, slug):
    """
    Handle the request to get a blog post by slug.
    Returns a text response with the post slug in the message.
    """
    return text_response(f"Post slug: {slug}")

# Define route for "/welcome" that responds with HTML content
@path("/welcome")  # Default is GET method
def welcome_view(req, method):
    """
    Handle the request for the welcome page.
    Returns an HTML response with a simple greeting.
    """
    html = "<div>Hi</div>"  # HTML content
    return html_response(html, status=status_codes.HTTP_200_OK)

# Define route for "/about-template" that responds with a rendered HTML template
@path("/about-template")  # Default is GET method
def about_template(req, method):
    """
    Handle the request for the about page using a template.
    Renders the "about.html" template and returns it as a response.
    """
    template_name = "about.html"  # Template file name
    return template_response(template_name, status=status_codes.HTTP_200_OK)

@path("/test-template")
def template_demo(req, method):
    """Demo route to showcase template features."""
    context = {
        "user": {
            "name": "john doe",
            "email": "JOHN.DOE@EXAMPLE.COM",
            "role": "moderator",
            "is_active": True,
            "join_date": datetime(2024, 1, 15),
            "bio": "This is a very long bio that will be truncated to demonstrate the truncate filter. It should show an ellipsis at the end.",
            "empty_field": "",
            "html_content": "<strong>This is bold text</strong> and <script>alert('xss')</script>"
        },
        "items": [
            {"name": "premium laptop", "price": 1299.99},
            {"name": "wireless mouse", "price": 29.99},
            {"name": "gaming keyboard", "price": 149.50},
            {"name": "monitor", "price": 299.99},
            {"name": "usb cable", "price": 9.99}
        ]
    }
    return template_response("test_template.html", context)
