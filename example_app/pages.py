# app.py
from core.path import path
from response.main import text_response, html_response, template_response
from response import status_codes

@path("/", methods=["GET"])
def home(req, method):
    return text_response("Welcome to the homepage!", status=status_codes.HTTP_200_OK)

@path("/about")
def about(req, method):
    return "This is the about page."

@path("/user/<id>")
def get_user(req, method, id):
    return f"User ID is: {id}"

@path("/post/<slug>", methods=["GET"])
def get_post(req, method, slug):
    return text_response(f"Post slug: {slug}")

@path("/welcome")
def welcome_view(req, method):
    html = "<div>Hi</div>"
    return html_response(html, status=status_codes.HTTP_200_OK)

@path("/about-template")
def about(req, method):
    template_name = "about.html"
    return template_response(template_name, status=status_codes.HTTP_200_OK)