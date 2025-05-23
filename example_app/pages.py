# app.py
from nublar.path import path  # Import the 'path' decorator to define URL routes
from response.http_response import text_response, html_response, template_response  # Import response functions
from response import status_codes  # Import HTTP status codes

# Define route for "/homepage" that responds with a text message
@path("/homepage", methods=["GET"])  # Only allows GET method
def home(req, method):
    """
    Handle the GET request for the homepage.
    Returns a simple text response with a 200 OK status.
    """
    return text_response("Welcome to the homepage!", status=status_codes.HTTP_200_OK)

# Define route for "/about" that responds with a text message
@path("/about")  # Default is GET method
def about(req, method):
    """
    Handle the request for the about page.
    Returns a simple text response indicating this is the about page.
    """
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
