from http.cookies import SimpleCookie

# Utility to set a cookie
def set_cookie(name, value, max_age=None, expires=None, path="/", domain=None, secure=False, httponly=False):
    """
    Sets a cookie with various options.

    Arguments:
        name: The name of the cookie.
        value: The value to store in the cookie.
        max_age: The maximum age of the cookie in seconds (optional).
        expires: The expiration date of the cookie (optional).
        path: The path where the cookie is valid (default is "/").
        domain: The domain for which the cookie is valid (optional).
        secure: If True, the cookie will only be sent over HTTPS (optional).
        httponly: If True, the cookie cannot be accessed by JavaScript (optional).

    Returns:
        The cookie header string to be sent in the HTTP response.
    """
    cookie = SimpleCookie()  # Create a new cookie object
    cookie[name] = value  # Set the cookie value

    # Set optional cookie attributes
    if max_age:
        cookie[name]["Max-Age"] = max_age
    if expires:
        cookie[name]["Expires"] = expires
    cookie[name]["Path"] = path  # Default is "/"
    if domain:
        cookie[name]["Domain"] = domain
    if secure:
        cookie[name]["Secure"] = True  # Cookie will be sent over HTTPS only
    if httponly:
        cookie[name]["HttpOnly"] = True  # Cookie can't be accessed via JavaScript

    # Return the cookie header as a string
    return cookie.output(header="", sep="").strip()

# Utility to delete a cookie
def delete_cookie(name, path="/"):
    """
    Deletes a cookie by setting its 'Max-Age' to 0.

    Arguments:
        name: The name of the cookie to delete.
        path: The path where the cookie is valid (default is "/").

    Returns:
        The cookie header string to delete the cookie.
    """
    # To delete a cookie, set its Max-Age to 0 (expires immediately)
    return set_cookie(name, "", max_age=0, path=path)

# Utility to get a cookie from the request
def get_cookie(req, name):
    """
    Retrieves the value of a cookie from the request.

    Arguments:
        req: The HTTP request object.
        name: The name of the cookie to retrieve.

    Returns:
        The value of the cookie, or None if the cookie is not found.
    """
    cookies = req.headers.get("Cookie", "")  # Get the cookie header from the request
    cookie = SimpleCookie(cookies)  # Parse the cookie string into a SimpleCookie object
    return cookie.get(name) and cookie[name].value or None  # Return the value of the cookie or None if not found