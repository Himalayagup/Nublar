import time
from http.cookies import SimpleCookie
import json

# Utility to set a cookie
def set_cookie(name, value, max_age=None, expires=None, path="/", domain=None, secure=False, httponly=False):
    cookie = SimpleCookie()
    cookie[name] = value

    if max_age:
        cookie[name]["Max-Age"] = max_age
    if expires:
        cookie[name]["Expires"] = expires
    cookie[name]["Path"] = path
    if domain:
        cookie[name]["Domain"] = domain
    if secure:
        cookie[name]["Secure"] = True
    if httponly:
        cookie[name]["HttpOnly"] = True

    # Return the cookie header as a string
    return cookie.output(header="", sep="").strip()

# Utility to delete a cookie
def delete_cookie(name, path="/"):
    # To delete a cookie, set its Max-Age to 0
    return set_cookie(name, "", max_age=0, path=path)

# Utility to get a cookie from the request
def get_cookie(req, name):
    cookies = req.headers.get("Cookie", "")
    cookie = SimpleCookie(cookies)
    return cookie.get(name) and cookie[name].value or None
