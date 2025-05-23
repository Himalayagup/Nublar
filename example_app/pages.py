# app.py
from core.path import path
from response.main import json_response, text_response

@path("/", methods=["GET"])
def home(req, method):
    return text_response("Welcome to the homepage!", status=200)

@path("/about")
def about(req, method):
    return "This is the about page."

@path("/user/<id>")
def get_user(req, method, id):
    return f"User ID is: {id}"

@path("/post/<slug>", methods=["GET"])
def get_post(req, method, slug):
    return text_response(f"Post slug: {slug}")