# app.py
from nublar.cookies import set_cookie, get_cookie, delete_cookie  # Import cookie utility functions
from response.http_response import text_response, json_response  # Import response functions
from nublar.path import path  # Import the path decorator for defining URL routes

# Set a Cookie - This route sets a cookie for the user
@path("/set-cookie")
def set_cookie_view(req, method):
    """
    Handles the '/set-cookie' route to set a cookie.
    - Sets a cookie called 'username' with value 'Himalaya' that expires in 1 hour (3600 seconds).
    - The cookie is added to the response header.
    """
    # Set the cookie with a max-age of 3600 seconds (1 hour)
    cookie_header = set_cookie("username", "Himalaya", max_age=3600)

    # Create a response to inform the user that the cookie has been set
    response = text_response("Cookie has been set!")

    # Add the cookie header to the response
    response.add_cookie(cookie_header)

    return response  # Return the response with the cookie set

# Get a Cookie - This route retrieves the cookie value
@path("/get-cookie")
def get_cookie_view(req, method):
    """
    Handles the '/get-cookie' route to retrieve a cookie.
    - Checks if the 'username' cookie exists and returns its value.
    - If the cookie is not found, it returns a message indicating no cookie was found.
    """
    # Retrieve the 'username' cookie from the request
    username = get_cookie(req, "username")

    # Check if the cookie exists and return an appropriate message
    if username:
        return text_response(f"Hello, {username}!")  # If cookie exists, greet the user
    else:
        return text_response("No username cookie found.")  # If cookie doesn't exist, notify the user

# Delete a Cookie - This route deletes the cookie
@path("/delete-cookie")
def delete_cookie_view(req, method):
    """
    Handles the '/delete-cookie' route to delete a cookie.
    - Deletes the 'username' cookie by setting its max-age to 0.
    - Adds the delete cookie header to the response to inform the client.
    """
    # Delete the 'username' cookie
    cookie_header = delete_cookie("username")

    # Create a response to inform the user that the cookie has been deleted
    response = text_response("Cookie has been deleted yay!")

    # Add the delete cookie header to the response to ensure it's deleted on the client-side
    response.add_cookie(cookie_header)

    return response  # Return the response with the cookie deletion header
