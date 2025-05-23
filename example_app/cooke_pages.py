from core.cookies import set_cookie, get_cookie, delete_cookie
from response.main import text_response, json_response
from core.path import path

# Set a Cookie
@path("/set-cookie")
def set_cookie_view(req, method):
    cookie_header = set_cookie("username", "Himalaya", max_age=3600)
    response = text_response("Cookie has been set!")
    response.add_cookie(cookie_header)  # Add the cookie header to the response
    return response

# Get a Cookie
@path("/get-cookie")
def get_cookie_view(req, method):
    username = get_cookie(req, "username")
    if username:
        return text_response(f"Hello, {username}!")
    else:
        return text_response("No username cookie found.")

# Delete a Cookie
@path("/delete-cookie")
def delete_cookie_view(req, method):
    cookie_header = delete_cookie("username")
    response = text_response("Cookie has been deleted!")
    response.add_cookie(cookie_header)  # Add the delete cookie header to the response
    return response
