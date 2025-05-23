# app.py
from core.path import path
from response.main import json_response, text_response

BASE_PATH = "v1"


@path("/submit")
def submit_data(req, method, data):
    name = data.get("name") or "Anonymous"
    if isinstance(name, list):
        name = name[0]
    return f"Received name: {name}"

@path("/api", methods=["GET", "POST"])
def api_data(req, method, data=None):
    if method == "POST":
        return text_response(f"Success Post Request")
    return json_response({"message": "Hello There"}, status=200)

